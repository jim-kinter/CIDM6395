from django.contrib import admin
from .models import (
    Material, Requirement, InstallationRequirement, Widget, Shipment,
    Inspection, MaintenanceRecord, InventoryRecord, CustomerOrder
)

# Register all MMS models
admin.site.register(Material)
admin.site.register(Requirement)
admin.site.register(InstallationRequirement)
admin.site.register(Widget)
admin.site.register(Shipment)
admin.site.register(Inspection)
admin.site.register(MaintenanceRecord)
admin.site.register(InventoryRecord)
admin.site.register(CustomerOrder)