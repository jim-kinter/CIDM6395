from django.db import models
import uuid

class MaterialStatus(models.TextChoices):
    RECEIVED = "Received", "Received"
    INSPECTED = "Inspected", "Inspected"
    STORED = "Stored", "Stored"
    ISSUED = "Issued", "Issued"
    SHIPPED = "Shipped", "Shipped"

class RequirementStatus(models.TextChoices):
    DRAFT = "Draft", "Draft"
    FEEDBACK = "Feedback", "Feedback"
    FINALIZED = "Finalized", "Finalized"

class WidgetStatus(models.TextChoices):
    FABRICATED = "Fabricated", "Fabricated"
    INSPECTED = "Inspected", "Inspected"
    SHIPPED = "Shipped", "Shipped"

class ShipmentStatus(models.TextChoices):
    PREPARED = "Prepared", "Prepared"
    SHIPPED = "Shipped", "Shipped"
    DELIVERED = "Delivered", "Delivered"

class InspectionResult(models.TextChoices):
    PASS = "Pass", "Pass"
    FAIL = "Fail", "Fail"

class Material(models.Model):
    material_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=100)
    quantity = models.IntegerField()
    status = models.CharField(max_length=50, choices=MaterialStatus.choices, default=MaterialStatus.RECEIVED)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} ({self.material_id})"

class Requirement(models.Model):
    req_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    material_id = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    delivery_date = models.DateField()
    status = models.CharField(max_length=50, choices=RequirementStatus.choices, default=RequirementStatus.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Requirement {self.req_id} for {self.material_id}"

class InstallationRequirement(models.Model):
    inst_req_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    material_id = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    fab_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Installation Requirement {self.inst_req_id} for {self.material_id}"

class Widget(models.Model):
    widget_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    material_id = models.ForeignKey(Material, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=WidgetStatus.choices, default=WidgetStatus.FABRICATED)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Widget {self.widget_id} from {self.material_id}"

class Shipment(models.Model):
    shipment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    material_id = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, blank=True)
    widget_id = models.ForeignKey(Widget, on_delete=models.SET_NULL, null=True, blank=True)
    tracking_id = models.CharField(max_length=50)
    customer_id = models.CharField(max_length=50)
    status = models.CharField(max_length=50, choices=ShipmentStatus.choices, default=ShipmentStatus.PREPARED)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Shipment {self.shipment_id} ({self.tracking_id})"

class Inspection(models.Model):
    inspection_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    material_id = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, blank=True)
    widget_id = models.ForeignKey(Widget, on_delete=models.SET_NULL, null=True, blank=True)
    result = models.CharField(max_length=50, choices=InspectionResult.choices)
    defects = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inspection {self.inspection_id}"

class MaintenanceRecord(models.Model):
    maint_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    material_id = models.ForeignKey(Material, on_delete=models.CASCADE)
    date = models.DateField()
    condition = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Maintenance {self.maint_id} for {self.material_id}"

class InventoryRecord(models.Model):
    inv_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    material_id = models.ForeignKey(Material, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    last_checked = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inventory {self.inv_id} for {self.material_id}"

class CustomerOrder(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    material_id = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, blank=True)
    widget_id = models.ForeignKey(Widget, on_delete=models.SET_NULL, null=True, blank=True)
    customer_id = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_id} for Customer {self.customer_id}"