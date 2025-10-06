from rest_framework import serializers
from .models import (
    Material, Requirement, InstallationRequirement, Widget, Shipment,
    Inspection, MaintenanceRecord, InventoryRecord, CustomerOrder,
    MaterialStatus, RequirementStatus, WidgetStatus, ShipmentStatus, InspectionResult
)

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['material_id', 'type', 'quantity', 'status', 'created_at']
        read_only_fields = ['material_id', 'created_at']

class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        fields = ['req_id', 'material_id', 'quantity', 'delivery_date', 'status', 'created_at']
        read_only_fields = ['req_id', 'created_at']

class InstallationRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstallationRequirement
        fields = ['inst_req_id', 'material_id', 'quantity', 'fab_date', 'created_at']
        read_only_fields = ['inst_req_id', 'created_at']

class WidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Widget
        fields = ['widget_id', 'material_id', 'status', 'created_at']
        read_only_fields = ['widget_id', 'created_at']

class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = ['shipment_id', 'material_id', 'widget_id', 'tracking_id', 'customer_id', 'status', 'created_at']
        read_only_fields = ['shipment_id', 'created_at']

class InspectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inspection
        fields = ['inspection_id', 'material_id', 'widget_id', 'result', 'defects', 'created_at']
        read_only_fields = ['inspection_id', 'created_at']

class MaintenanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceRecord
        fields = ['maint_id', 'material_id', 'date', 'condition', 'created_at']
        read_only_fields = ['maint_id', 'created_at']

class InventoryRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryRecord
        fields = ['inv_id', 'material_id', 'location', 'last_checked', 'created_at']
        read_only_fields = ['inv_id', 'created_at']

class CustomerOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerOrder
        fields = ['order_id', 'material_id', 'widget_id', 'customer_id', 'status', 'created_at']
        read_only_fields = ['order_id', 'created_at']