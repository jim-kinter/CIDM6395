
from django.test import TestCase
from rest_framework.test import APIClient
from .models import (
    Material, Requirement, InstallationRequirement, Widget, Shipment,
    Inspection, MaintenanceRecord, InventoryRecord, CustomerOrder
)
import uuid
from unittest.mock import patch

class MMSTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.material = Material.objects.create(
            material_id=uuid.uuid4(),
            type="steel",
            quantity=100,
            status="Stored"
        )
        self.requirement = Requirement.objects.create(
            req_id=uuid.uuid4(),
            material_id=self.material,
            quantity=100,
            delivery_date="2025-06-01",
            status="Draft"
        )
        self.installation_requirement = InstallationRequirement.objects.create(
            inst_req_id=uuid.uuid4(),
            material_id=self.material,
            quantity=50,
            fab_date="2025-06-15"
        )
        self.widget = Widget.objects.create(
            widget_id=uuid.uuid4(),
            material_id=self.material,
            status="Fabricated"
        )
        self.shipment = Shipment.objects.create(
            shipment_id=uuid.uuid4(),
            widget_id=self.widget,
            tracking_id="T123",
            customer_id="C456",
            status="Shipped"
        )
        self.inspection = Inspection.objects.create(
            inspection_id=uuid.uuid4(),
            material_id=self.material,
            result="Fail",
            defects=""
        )
        self.maintenance_record = MaintenanceRecord.objects.create(
            maint_id=uuid.uuid4(),
            material_id=self.material,
            date="2025-06-10",
            condition="pending"
        )
        self.inventory_record = InventoryRecord.objects.create(
            inv_id=uuid.uuid4(),
            material_id=self.material,
            location="Aisle 5",
            last_checked="2025-06-01"
        )
        self.customer_order = CustomerOrder.objects.create(
            order_id=uuid.uuid4(),
            widget_id=self.widget,
            customer_id="C789",
            status="Shipped"
        )

    # Material Tests
    @patch('apps.views.notify_warehouse_task.delay')
    def test_create_material_arrival(self, mock_notify):
        response = self.client.post(
            '/api/materials/arrival/',
            {"shipment_id": "S456", "material_type": "aluminum", "quantity": 200},
            format='json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['status'], "Received")
        mock_notify.assert_called_once_with("Inspection task assigned for material arrival.")

    def test_update_material_storage(self):
        response = self.client.put(
            f'/api/materials/{self.material.material_id}/store/',
            {"location": "Aisle 5"},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        material = Material.objects.get(material_id=self.material.material_id)
        self.assertEqual(material.status, "Stored")

    @patch('apps.views.notify_fabrication_task.delay')
    def test_issue_material(self, mock_notify):
        response = self.client.post(
            '/api/materials/issue/',
            {"material_id": str(self.material.material_id), "quantity": 50},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        material = Material.objects.get(material_id=self.material.material_id)
        self.assertEqual(material.status, "Issued")
        self.assertEqual(material.quantity, 50)
        mock_notify.assert_called_once_with(f"Material {self.material.material_id} issued for fabrication.")

    def test_delete_material(self):
        response = self.client.delete(f'/api/materials/{self.material.material_id}/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Material.objects.filter(material_id=self.material.material_id).exists())

    @patch('apps.views.generate_demand_report_task.delay')
    def test_generate_material_demand_report(self, mock_task):
        response = self.client.post(
            '/api/materials/report/',
            {"start_date": "2025-06-01", "end_date": "2025-06-30"},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], "Generating")
        mock_task.assert_called_once()

    # Requirement Tests
    @patch('apps.views.notify_procurement_task.delay')
    def test_submit_requirement(self, mock_notify):
        response = self.client.post(
            '/api/requirements/',
            {
                "material_id": str(self.material.material_id),
                "quantity": 50,
                "delivery_date": "2025-06-01"
            },
            format='json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['status'], "Draft")
        mock_notify.assert_called_once()

    @patch('apps.views.notify_engineer_task.delay')
    def test_provide_requirement_feedback(self, mock_notify):
        response = self.client.post(
            f'/api/requirements/{self.requirement.req_id}/feedback/',
            {"availability": "limited", "lead_time": "2 weeks"},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], "Feedback")
        mock_notify.assert_called_once()

    @patch('apps.views.notify_fabrication_task.delay')
    def test_finalize_requirement(self, mock_notify):
        self.requirement.status = "Feedback"
        self.requirement.save()
        response = self.client.put(
            f'/api/requirements/{self.requirement.req_id}/',
            {
                "material_id": str(self.material.material_id),
                "quantity": 80,
                "delivery_date": "2025-06-15"
            },
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], "Finalized")
        mock_notify.assert_called_once()

    # InstallationRequirement Tests
    @patch('apps.views.notify_warehouse_task.delay')
    def test_submit_installation_requirement(self, mock_notify):
        response = self.client.post(
            '/api/installation_requirements/',
            {"material_id": str(self.material.material_id), "quantity": 60, "fab_date": "2025-06-15"},
            format='json'
        )
        self.assertEqual(response.status_code, 201)
        mock_notify.assert_called_once()

    def test_update_installation_requirement(self):
        response = self.client.put(
            f'/api/installation_requirements/{self.installation_requirement.inst_req_id}/',
            {
                "material_id": str(self.material.material_id),
                "quantity": 70,
                "fab_date": "2025-06-16"
            },
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        updated = InstallationRequirement.objects.get(inst_req_id=self.installation_requirement.inst_req_id)
        self.assertEqual(updated.quantity, 70)

    # Widget Tests
    def test_create_widget(self):
        self.material.status = "Issued"
        self.material.save()
        response = self.client.post(
            '/api/widgets/',
            {"material_id": str(self.material.material_id), "status": "Fabricated"},
            format='json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['status'], "Fabricated")

    def test_update_widget_status(self):
        response = self.client.put(
            f'/api/widgets/{self.widget.widget_id}/',
            {
                "material_id": str(self.material.material_id),
                "status": "Inspected"
            },
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        updated = Widget.objects.get(widget_id=self.widget.widget_id)
        self.assertEqual(updated.status, "Inspected")

    # Shipment Tests
    @patch('apps.views.notify_shipping_task.delay')
    def test_prepare_shipment(self, mock_notify):
        self.widget.status = "Inspected"
        self.widget.save()
        response = self.client.post(
            '/api/shipments/',
            {"widget_id": str(self.widget.widget_id), "tracking_id": "T789", "customer_id": "C012"},
            format='json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['status'], "Shipped")
        mock_notify.assert_called_once()

    @patch('apps.views.notify_shipping_task.delay')
    def test_confirm_shipment_delivery(self, mock_notify):
        response = self.client.post(
            '/api/shipments/confirm/',
            {"shipment_id": str(self.shipment.shipment_id), "delivered": True},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        updated = Shipment.objects.get(shipment_id=self.shipment.shipment_id)
        self.assertEqual(updated.status, "Delivered")
        mock_notify.assert_called_once()

    # Inspection Tests
    @patch('apps.views.notify_warehouse_task.delay')
    def test_material_inspection_pass(self, mock_notify):
        self.material.status = "Received"
        self.material.save()
        response = self.client.post(
            '/api/inspections/',
            {
                "material_id": str(self.material.material_id),
                "result": "Pass",
                "defects": ""
            },
            format='json'
        )
        if response.status_code != 201:
          print("Response data:", response.data)  # Debug output
        self.assertEqual(response.status_code, 201)
        material = Material.objects.get(material_id=self.material.material_id)
        self.assertEqual(material.status, "Stored")
        mock_notify.assert_called_once()

    @patch('apps.views.notify_procurement_task.delay')
    def test_flag_material_defects(self, mock_notify):
        response = self.client.post(
            f'/api/inspections/{self.inspection.inspection_id}/flag/',
            {"defects": "cracks detected"},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], "Notified")
        mock_notify.assert_called_once()

    # MaintenanceRecord Tests
    def test_schedule_maintenance_task(self):
        response = self.client.post(
            '/api/maintenance/',
            {
                "material_id": str(self.material.material_id),
                "date": "2025-06-10",
                "condition": "pending"
            },
            format='json'
        )
        self.assertEqual(response.status_code, 201)

    def test_update_maintenance_condition(self):
        response = self.client.put(
            f'/api/maintenance/{self.maintenance_record.maint_id}/',
            {
                "material_id": str(self.material.material_id),
                "date": "2025-06-10",
                "condition": "good"
            },
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        updated = MaintenanceRecord.objects.get(maint_id=self.maintenance_record.maint_id)
        self.assertEqual(updated.condition, "good")

    # InventoryRecord Tests
    def test_create_inventory_record(self):
        response = self.client.post(
            '/api/inventory/',
            {"material_id": str(self.material.material_id), "location": "Aisle 5", "last_checked": "2025-06-01"},
            format='json'
        )
        self.assertEqual(response.status_code, 201)

    def test_update_inventory_location(self):
        response = self.client.put(
            f'/api/inventory/{self.inventory_record.inv_id}/',
            {
                "material_id": str(self.material.material_id),
                "location": "Aisle 6",
                "last_checked": "2025-06-01"
            },
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        updated = InventoryRecord.objects.get(inv_id=self.inventory_record.inv_id)
        self.assertEqual(updated.location, "Aisle 6")

    # CustomerOrder Tests
    def test_create_customer_order(self):
        self.widget.status = "Inspected"
        self.widget.save()
        response = self.client.post(
            '/api/orders/',
            {"widget_id": str(self.widget.widget_id), "customer_id": "C789", "status": "Pending"},
            format='json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['status'], "Pending")

    def test_confirm_customer_order_receipt(self):
        response = self.client.post(
            '/api/orders/confirm/',
            {"order_id": str(self.customer_order.order_id), "received": True},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        updated = CustomerOrder.objects.get(order_id=self.customer_order.order_id)
        self.assertEqual(updated.status, "Received")

    def test_calculate_order_progress(self):
        response = self.client.get(f'/api/orders/{self.customer_order.order_id}/progress/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['progress_percentage'], 75)
        self.assertEqual(response.data['status'], "Shipped")