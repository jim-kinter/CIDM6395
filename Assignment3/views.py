from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import (
    Material, Requirement, InstallationRequirement, Widget, Shipment,
    Inspection, MaintenanceRecord, InventoryRecord, CustomerOrder
)
from .serializers import (
    MaterialSerializer, RequirementSerializer, InstallationRequirementSerializer,
    WidgetSerializer, ShipmentSerializer, InspectionSerializer,
    MaintenanceRecordSerializer, InventoryRecordSerializer, CustomerOrderSerializer
)
from .tasks import notify_procurement_task, notify_engineer_task, notify_fabrication_task, notify_warehouse_task, notify_shipping_task, generate_demand_report_task, send_notification_task
import uuid

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

    @action(detail=False, methods=['post'])
    def arrival(self, request):
        # Map material_type to type for serializer compatibility
        data = request.data.copy()  # Create a mutable copy of the request data
        if 'material_type' in data:
            data['type'] = data.pop('material_type')  # Rename material_type to type
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save(status="Received")
            # Trigger Celery task for inspection
            notify_warehouse_task.delay("Inspection task assigned for material arrival.")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def store(self, request, pk=None):
        material = self.get_object()
        location = request.data.get('location')
        if location:
            material.status = "Stored"
            material.save()
            serializer = self.get_serializer(material)
            return Response(serializer.data)
        return Response({"error": "Location required"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def issue(self, request):
        material_id = request.data.get('material_id')
        quantity = request.data.get('quantity')
        try:
            material = Material.objects.get(material_id=material_id)
            if material.quantity >= quantity:
                material.status = "Issued"
                material.quantity -= quantity
                material.save()
                serializer = self.get_serializer(material)
                notify_fabrication_task.delay(f"Material {material_id} issued for fabrication.")
                return Response(serializer.data)
            return Response({"error": "Insufficient quantity"}, status=status.HTTP_400_BAD_REQUEST)
        except Material.DoesNotExist:
            return Response({"error": "Material not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def report(self, request):
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        if start_date and end_date:
            report_id = str(uuid.uuid4())
            generate_demand_report_task.delay(report_id, start_date, end_date)
            return Response({"report_id": report_id, "status": "Generating"})
        return Response({"error": "Start and end dates required"}, status=status.HTTP_400_BAD_REQUEST)

class RequirementViewSet(viewsets.ModelViewSet):
    queryset = Requirement.objects.all()
    serializer_class = RequirementSerializer

    def perform_create(self, serializer):
        instance = serializer.save(status="Draft")
        notify_procurement_task.delay(f"New requirement {instance.req_id} created.")

    @action(detail=True, methods=['post'])
    def feedback(self, request, pk=None):
        requirement = self.get_object()
        availability = request.data.get('availability')
        lead_time = request.data.get('lead_time')
        if availability and lead_time:
            requirement.status = "Feedback"
            requirement.save()
            serializer = self.get_serializer(requirement)
            notify_engineer_task.delay(f"Feedback received for requirement {requirement.req_id}.")
            return Response(serializer.data)
        return Response({"error": "Availability and lead_time required"}, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        instance = serializer.save(status="Finalized")
        notify_fabrication_task.delay(f"Requirement {instance.req_id} finalized.")

class InstallationRequirementViewSet(viewsets.ModelViewSet):
    queryset = InstallationRequirement.objects.all()
    serializer_class = InstallationRequirementSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        notify_warehouse_task.delay(f"Installation requirement {instance.inst_req_id} created for fabrication.")

class WidgetViewSet(viewsets.ModelViewSet):
    queryset = Widget.objects.all()
    serializer_class = WidgetSerializer

class ShipmentViewSet(viewsets.ModelViewSet):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer

    def perform_create(self, serializer):
        instance = serializer.save(status="Shipped")
        notify_shipping_task.delay(f"Shipment {instance.shipment_id} prepared.")

    @action(detail=False, methods=['post'])
    def confirm(self, request):
        shipment_id = request.data.get('shipment_id')
        delivered = request.data.get('delivered')
        try:
            shipment = Shipment.objects.get(shipment_id=shipment_id)
            if delivered:
                shipment.status = "Delivered"
                shipment.save()
                serializer = self.get_serializer(shipment)
                notify_shipping_task.delay(f"Shipment {shipment_id} delivered.")
                return Response(serializer.data)
            return Response({"error": "Delivered status required"}, status=status.HTTP_400_BAD_REQUEST)
        except Shipment.DoesNotExist:
            return Response({"error": "Shipment not found"}, status=status.HTTP_404_NOT_FOUND)

class InspectionViewSet(viewsets.ModelViewSet):
    queryset = Inspection.objects.all()
    serializer_class = InspectionSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        if instance.material_id:
            material = instance.material_id
            material.status = "Stored" if instance.result == "Pass" else "Flagged"
            material.save()
            notify_warehouse_task.delay(f"Inspection {instance.inspection_id} completed for material.")
        elif instance.widget_id:
            widget = instance.widget_id
            widget.status = "Ready for Shipping" if instance.result == "Pass" else "Flagged"
            widget.save()
            notify_shipping_task.delay(f"Inspection {instance.inspection_id} completed for widget.")

    @action(detail=True, methods=['post'])
    def flag(self, request, pk=None):
        inspection = self.get_object()
        defects = request.data.get('defects')
        if defects:
            if inspection.material_id:
                notify_procurement_task.delay(f"Material flagged with defects: {defects}")
            elif inspection.widget_id:
                notify_fabrication_task.delay(f"Widget flagged with defects: {defects}")
            return Response({"status": "Notified"})
        return Response({"error": "Defects required"}, status=status.HTTP_400_BAD_REQUEST)

class MaintenanceRecordViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRecord.objects.all()
    serializer_class = MaintenanceRecordSerializer

class InventoryRecordViewSet(viewsets.ModelViewSet):
    queryset = InventoryRecord.objects.all()
    serializer_class = InventoryRecordSerializer

class CustomerOrderViewSet(viewsets.ModelViewSet):
    queryset = CustomerOrder.objects.all()
    serializer_class = CustomerOrderSerializer

    @action(detail=False, methods=['post'])
    def confirm(self, request):
        order_id = request.data.get('order_id')
        received = request.data.get('received')
        try:
            order = CustomerOrder.objects.get(order_id=order_id)
            if received:
                order.status = "Received"
                order.save()
                serializer = self.get_serializer(order)
                return Response(serializer.data)
            return Response({"error": "Received status required"}, status=status.HTTP_400_BAD_REQUEST)
        except CustomerOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def progress(self, request, pk=None):
        order = self.get_object()
        progress = 75 if order.status == "Shipped" else 100 if order.status == "Received" else 50
        return Response({"order_id": str(order.order_id), "progress_percentage": progress, "status": order.status})

class NotificationViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def notify(self, request):
        recipient_id = request.data.get('recipient_id')
        message = request.data.get('message')
        if recipient_id and message:
            notification_id = str(uuid.uuid4())
            send_notification_task.delay(recipient_id, message)
            return Response({"notification_id": notification_id, "status": "Sent"})
        return Response({"error": "Recipient ID and message required"}, status=status.HTTP_400_BAD_REQUEST)