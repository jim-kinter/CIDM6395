from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MaterialViewSet, RequirementViewSet, InstallationRequirementViewSet,
    WidgetViewSet, ShipmentViewSet, InspectionViewSet,
    MaintenanceRecordViewSet, InventoryRecordViewSet,
    CustomerOrderViewSet, NotificationViewSet
)

router = DefaultRouter()
router.register(r'materials', MaterialViewSet)
router.register(r'requirements', RequirementViewSet)
router.register(r'installation_requirements', InstallationRequirementViewSet)
router.register(r'widgets', WidgetViewSet)
router.register(r'shipments', ShipmentViewSet)
router.register(r'inspections', InspectionViewSet)
router.register(r'maintenance', MaintenanceRecordViewSet)
router.register(r'inventory', InventoryRecordViewSet)
router.register(r'orders', CustomerOrderViewSet)
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
]