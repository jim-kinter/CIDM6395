# MMS Evolution 2 API Design

## Overview

The Materials Management System (MMS) API, built with Django REST Framework (DRF), enables seamless management of material demand and tracking in the context of industrial manufacturing. It supports daily material requirements from Engineering, installation requirements from Fabrication, and a feedback loop between Procurement and Engineering to finalize specifications. The API tracks materials from dock arrival to customer delivery, serving personas: Engineer, Fabrication, Procurement, Sales, Warehouse, Inventory, Shipping, Inspection, Preventative Maintenance, and Quality Control. Hosted at `http://localhost:8000/api/`, it uses Django ORM with SQLite (`Evolution_1/mms/mms.db`), Celery with Redis in Docker for asynchronous tasks, and DRF serializers for validation. This document defines CRUD and beyond CRUD endpoints, along with an Entity-Relationship Diagram (ERD) for MMS entities, aligning with the Evolution 1 Class Diagram requirement (`artifacts/Class_Diagram_r1.png`).

## API Endpoints

The MMS API provides RESTful endpoints for CRUD operations on entities and beyond CRUD operations for reports, notifications, and progress tracking. All endpoints are prefixed with `/api/` and require DRF token authentication for write operations. Responses use JSON, with standard HTTP status codes (e.g., 200 OK, 400 Bad Request, 404 Not Found).

### Entity: Material

- **Description**: Represents raw materials (e.g., steel, pipe, engineered equipment) tracked from arrival to issuance.
- **Endpoints**:
  - `GET /api/materials/`: List all materials (filterable by `?status=Stored`).
    - Response: `[{"material_id": "uuid", "type": "steel", "quantity": 100, "status": "Stored", ...}, ...]`
    - Status: 200 OK
  - `GET /api/materials/{material_id}/`: Retrieve a material by ID.
    - Response: `{"material_id": "uuid", "type": "steel", "quantity": 100, "status": "Stored", ...}`
    - Status: 200 OK or 404 Not Found
  - `POST /api/materials/arrival/`: Log material arrival at the dock.
    - Request: `{"shipment_id": "S123", "material_type": "steel", "quantity": 100}`
    - Response: `{"material_id": "uuid", "status": "Received", ...}`
    - Status: 201 Created or 400 Bad Request
  - `PUT /api/materials/{material_id}/store/`: Update material storage location.
    - Request: `{"location": "Aisle 5"}`
    - Response: `{"material_id": "uuid", "status": "Stored", "location": "Aisle 5", ...}`
    - Status: 200 OK or 404 Not Found
  - `POST /api/materials/issue/`: Issue materials for Fabrication.
    - Request: `{"material_id": "uuid", "quantity": 50}`
    - Response: `{"material_id": "uuid", "status": "Issued", ...}`
    - Status: 200 OK or 400 Bad Request
  - `DELETE /api/materials/{material_id}/`: Delete a material (admin only).
    - Status: 204 No Content or 404 Not Found

### Entity: Requirement

- **Description**: Represents Engineering’s material requirements, with feedback from Procurement.
- **Endpoints**:
  - `GET /api/requirements/`: List all requirements (filterable by `?status=Finalized`).
  - `GET /api/requirements/{req_id}/`: Retrieve a requirement by ID.
  - `POST /api/requirements/`: Submit a new requirement.
    - Request: `{"material_type": "steel", "quantity": 100, "delivery_date": "2025-06-01"}`
    - Response: `{"req_id": "uuid", "status": "Draft", ...}`
  - `POST /api/requirements/{req_id}/feedback/`: Submit Procurement feedback.
    - Request: `{"availability": "limited", "lead_time": "2 weeks"}`
    - Response: `{"req_id": "uuid", "status": "Feedback", ...}`
  - `PUT /api/requirements/{req_id}/`: Revise and finalize a requirement.
    - Request: `{"quantity": 80, "delivery_date": "2025-06-15"}`
    - Response: `{"req_id": "uuid", "status": "Finalized", ...}`
  - `DELETE /api/requirements/{req_id}/`: Delete a requirement (admin only).

### Entity: InstallationRequirement

- **Description**: Represents Fabrication’s material needs for widget production.
- **Endpoints**:
  - `GET /api/installation_requirements/`: List all installation requirements.
  - `GET /api/installation_requirements/{inst_req_id}/`: Retrieve an installation requirement.
  - `POST /api/installation_requirements/`: Submit a new installation requirement.
    - Request: `{"material_id": "uuid", "quantity": 50, "fab_date": "2025-06-15"}`
  - `PUT /api/installation_requirements/{inst_req_id}/`: Update an installation requirement.
  - `DELETE /api/installation_requirements/{inst_req_id}/`: Delete an installation requirement.

### Entity: Widget

- **Description**: Represents fabricated products from materials.
- **Endpoints**:
  - `GET /api/widgets/`: List all widgets.
  - `GET /api/widgets/{widget_id}/`: Retrieve a widget.
  - `POST /api/widgets/`: Create a new widget post-fabrication.
    - Request: `{"material_id": "uuid", "status": "Fabricated"}`
  - `PUT /api/widgets/{widget_id}/`: Update widget status (e.g., after inspection).
  - `DELETE /api/widgets/{widget_id}/`: Delete a widget.

### Entity: Shipment

- **Description**: Represents shipments of materials or widgets to customers.
- **Endpoints**:
  - `GET /api/shipments/`: List all shipments.
  - `GET /api/shipments/{shipment_id}/`: Retrieve a shipment.
  - `POST /api/shipments/`: Prepare a new shipment.
    - Request: `{"widget_id": "uuid", "tracking_id": "T123", "customer_id": "C456"}`
  - `POST /api/shipments/confirm/`: Confirm customer receipt.
    - Request: `{"shipment_id": "uuid", "delivered": true}`
  - `DELETE /api/shipments/{shipment_id}/`: Delete a shipment.

### Entity: Inspection

- **Description**: Represents quality inspections for materials or widgets.
- **Endpoints**:
  - `GET /api/inspections/`: List all inspections.
  - `GET /api/inspections/{inspection_id}/`: Retrieve an inspection.
  - `POST /api/inspections/`: Submit inspection results.
    - Request: `{"material_id": "uuid", "result": "Pass", "defects": null}`
  - `POST /api/inspections/{inspection_id}/flag/`: Flag defective materials/widgets.
    - Request: `{"defects": "cracks detected"}`
  - `DELETE /api/inspections/{inspection_id}/`: Delete an inspection.

### Entity: MaintenanceRecord

- **Description**: Represents maintenance activities on stored materials.
- **Endpoints**:
  - `GET /api/maintenance/`: List all maintenance records.
  - `GET /api/maintenance/{maint_id}/`: Retrieve a maintenance record.
  - `POST /api/maintenance/`: Schedule a maintenance task.
    - Request: `{"material_id": "uuid", "date": "2025-06-10"}`
  - `PUT /api/maintenance/{maint_id}/`: Update maintenance condition.
    - Request: `{"condition": "good"}`
  - `DELETE /api/maintenance/{maint_id}/`: Delete a maintenance record.

### Entity: InventoryRecord

- **Description**: Represents inventory tracking for materials.
- **Endpoints**:
  - `GET /api/inventory/`: List all inventory records.
  - `GET /api/inventory/{inv_id}/`: Retrieve an inventory record.
  - `PUT /api/inventory/{inv_id}/`: Update inventory status/location.
    - Request: `{"status": "Stored", "location": "Aisle 5"}`
  - `DELETE /api/inventory/{inv_id}/`: Delete an inventory record.

### Entity: CustomerOrder

- **Description**: Represents customer orders for materials or widgets.
- **Endpoints**:
  - `GET /api/orders/`: List all customer orders.
  - `GET /api/orders/{order_id}/`: Retrieve an order.
  - `POST /api/orders/confirm/`: Confirm order receipt.
    - Request: `{"order_id": "uuid", "received": true}`
  - `DELETE /api/orders/{order_id}/`: Delete an order.

### Beyond-CRUD Operations

- **Generate Material Demand Report**:
  - `POST /api/materials/report/`:
    - Request: `{"start_date": "2025-06-01", "end_date": "2025-06-30"}`
    - Response: `{"report_id": "uuid", "materials_needed": [{"type": "steel", "quantity": 500}, ...], "status": "Generated"}`
    - Description: Aggregates `Requirement` and `InstallationRequirement` data, processed by a Celery task (`generate_demand_report_task`).

- **Send Notification**:
  - `POST /api/notifications/`:
    - Request: `{"recipient_id": "uuid", "message": "Material M123 flagged"}`
    - Response: `{"notification_id": "uuid", "status": "Sent"}`
    - Description: Sends notifications (e.g., feedback, inspection results) via a Celery task (`send_notification_task`).

- **Calculate Order Progress**:
  - `GET /api/orders/{order_id}/progress/`:
    - Response: `{"order_id": "uuid", "progress_percentage": 75, "status": "Shipped"}`
    - Description: Calculates progress based on `Shipment` and `CustomerOrder` statuses, executed synchronously.

## Entity-Relationship Diagram (ERD)

The ERD defines MMS entities, their attributes, and relationships, aligned with Django ORM models in `Evolution_1/mms/apps/models.py`. It reflects the Evolution 1 Class Diagram (`artifacts/Class_Diagram_r1.png`), with fields and constraints for SQLite (`Evolution_1/mms/mms.db`).

  ![Entity Relationship Diagram (ERD)](../artifacts/Entity_Relationship_Diagram_r1.png)  
  [Link to Use ER Diagram](../artifacts/Entity_Relationship_Diagram_r1.png)

### Entities and Attributes

- **Material**:
  - `material_id`: UUID (Primary Key)
  - `type`: CharField(max_length=100)
  - `quantity`: IntegerField
  - `status`: CharField(choices=["Received", "Inspected", "Stored", "Issued", "Shipped"])
  - `created_at`: DateTimeField(auto_now_add=True)

- **Requirement**:
  - `req_id`: UUID (Primary Key)
  - `material_id`: ForeignKey(Material, on_delete=CASCADE)
  - `quantity`: IntegerField
  - `delivery_date`: DateField
  - `status`: CharField(choices=["Draft", "Feedback", "Finalized"])
  - `created_at`: DateTimeField(auto_now_add=True)

- **InstallationRequirement**:
  - `inst_req_id`: UUID (Primary Key)
  - `material_id`: ForeignKey(Material, on_delete=CASCADE)
  - `quantity`: IntegerField
  - `fab_date`: DateField
  - `created_at`: DateTimeField(auto_now_add=True)

- **Widget**:
  - `widget_id`: UUID (Primary Key)
  - `material_id`: ForeignKey(Material, on_delete=CASCADE)
  - `status`: CharField(choices=["Fabricated", "Inspected", "Shipped"])
  - `created_at`: DateTimeField(auto_now_add=True)

- **Shipment**:
  - `shipment_id`: UUID (Primary Key)
  - `material_id`: ForeignKey(Material, on_delete=SET_NULL, null=True)
  - `widget_id`: ForeignKey(Widget, on_delete=SET_NULL, null=True)
  - `tracking_id`: CharField(max_length=50)
  - `customer_id`: CharField(max_length=50)
  - `status`: CharField(choices=["Prepared", "Shipped", "Delivered"])
  - `created_at`: DateTimeField(auto_now_add=True)

- **Inspection**:
  - `inspection_id`: UUID (Primary Key)
  - `material_id`: ForeignKey(Material, on_delete=SET_NULL, null=True)
  - `widget_id`: ForeignKey(Widget, on_delete=SET_NULL, null=True)
  - `result`: CharField(choices=["Pass", "Fail"])
  - `defects`: TextField(blank=True)
  - `created_at`: DateTimeField(auto_now_add=True)

- **MaintenanceRecord**:
  - `maint_id`: UUID (Primary Key)
  - `material_id`: ForeignKey(Material, on_delete=CASCADE)
  - `date`: DateField
  - `condition`: TextField
  - `created_at`: DateTimeField(auto_now_add=True)

- **InventoryRecord**:
  - `inv_id`: UUID (Primary Key)
  - `material_id`: ForeignKey(Material, on_delete=CASCADE)
  - `location`: CharField(max_length=100)
  - `last_checked`: DateField
  - `created_at`: DateTimeField(auto_now_add=True)

- **CustomerOrder**:
  - `order_id`: UUID (Primary Key)
  - `material_id`: ForeignKey(Material, on_delete=SET_NULL, null=True)
  - `widget_id`: ForeignKey(Widget, on_delete=SET_NULL, null=True)
  - `customer_id`: CharField(max_length=50)
  - `status`: CharField(max_length=50)
  - `created_at`: DateTimeField(auto_now_add=True)

### Relationships

- **Material**:
  - One-to-Many: `Requirement`, `InstallationRequirement`, `Widget`, `Shipment`, `Inspection`, `MaintenanceRecord`, `InventoryRecord`
- **CustomerOrder**:
  - Many-to-One: `Material`, `Widget`
- **Shipment**:
  - Many-to-One: `CustomerOrder`
  - One-to-Many: `Material`, `Widget`
- **Inspection**:
  - One-to-Many: `Material`, `Widget`

## Implementation Notes

- **Models**: Defined in `Evolution_1/mms/apps/models.py`, using Django ORM with UUID primary keys and enumerated status fields.
- **Serializers**: Defined in `Evolution_1/mms/apps/serializers.py`, using DRF serializers for validation and serialization (e.g., `MaterialSerializer`, `RequirementSerializer`).
- **Authentication**: DRF token authentication ensures secure access to write endpoints.
- **Asynchronous Tasks**: Celery tasks (e.g., `notify_procurement_task`, `generate_demand_report_task`) handle notifications and reports, with Redis as the message broker.
- **Database**: SQLite (`Evolution_1/mms/mms.db`) stores all entities, with migrations applied via `python manage.py migrate`.

## Next Steps

- **Evolution 4**: Implement DRF viewsets, URLs, and Celery tasks in `Evolution_1/mms/apps/views.py` and `Evolution_1/mms/urls.py` to activate the API.
- **Evolution 5**: Develop a Ubiquitous Language Glossary, Gherkin Notation for the three Use Cases, and Django unittests to validate system functionality.
