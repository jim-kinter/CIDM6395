# MMS Evolution 1 Requirements Specification

The Materials Management System (MMS) is a Django REST Framework (DRF) application designed to streamline material demand and tracking in industrial manufacturing. It integrates daily material requirements from Engineering and installation requirements from Fabrication, enabling a feedback loop between Procurement and Engineering to finalize specifications. MMS tracks materials from dock arrival through receiving, quality inspection, storage, preventative maintenance, requisition, inventory, widget fabrication, shipping, and customer delivery. Key personas include Engineer, Fabrication, Procurement, Sales, Warehouse, Inventory, Shipping, Inspection, Preventative Maintenance, and Quality Control. Built with Django ORM, SQLite (`mms.db`), Celery with Redis in Docker for asynchronous tasks, and a Django admin UI at `http://localhost:8000/admin/`, MMS supports CRUD endpoints (`/api/materials/`, `/api/requirements/`) and beyond-CRUD operations (demand reports, notifications, progress tracking). UML diagrams (PNG files) are stored in the `artifacts` folder at the project root. Evolution 1 diagrams are suffixed with `_r1` to distinguish from Evolution 0 diagrams, which remain available in `Evolution_0/requirements.md`.

## Problem Specification

Industrial manufacturing requires precise coordination of material demand across Engineering, Procurement, and Fabrication, with materials tracked through complex processes including inspection, storage, maintenance, and shipping. Disparate systems lead to fragmented data, manual reconciliations, and delays, resulting in errors, inefficiencies, and missed delivery deadlines. MMS addresses these challenges by aggregating data feeds from Engineering, Procurement, and Fabrication systems, providing real-time tracking of materials and widgets, and delivering analytics for demand alignment, inventory accuracy, and delivery timelines. This reduces operational risks, minimizes costs, and ensures timely customer fulfillment.

## Solution Organization

MMS leverages Django REST Framework for a scalable API, Django ORM for robust data management, and Celery with Redis in Docker for asynchronous task processing. The solution is structured as follows:

- **CRUD Operations**: Manage entities (`Material`, `Requirement`, `Widget`, etc.) via RESTful endpoints (e.g., `/api/materials/`, `/api/requirements/`), using DRF viewsets and serializers.
- **Beyond-CRUD Operations**: Generate material demand reports, send notifications, and calculate order progress, with Celery handling asynchronous tasks for scalability.
- **Admin UI**: Provide a user-friendly interface at `http://localhost:8000/admin/` for data management across all personas.
- **Analytics**: Deliver dashboards and reports for material status, demand forecasting, and delivery tracking, powered by Django ORM queries and Celery tasks.

## User Stories

User Stories capture persona needs with acceptance criteria in Given/When/Then format, ensuring testability and alignment with Django/DRF functionality.

1. **Engineer**:
   - **Story**: As an Engineer, I want to submit daily material requirements so that Procurement can order the correct materials.
     - **Acceptance Criteria**:
       - Given an authenticated Engineer, when they submit a POST request to `/api/requirements/` with JSON `{ "material_type": "steel", "quantity": 100, "delivery_date": "2025-06-01" }`, then MMS creates a `Requirement` model instance with status "Draft" and triggers a Celery task to notify Procurement.
       - Given invalid JSON (e.g., missing `quantity`), when submitted, then MMS returns a 400 Bad Request error with validation details.
   - **Story**: As an Engineer, I want to receive Procurement feedback on material availability and timing so that I can revise and finalize specifications.
     - **Acceptance Criteria**:
       - Given a submitted `Requirement`, when Procurement submits feedback via `POST /api/requirements/{req_id}/feedback/` with JSON `{ "availability": "limited", "lead_time": "2 weeks" }`, then MMS updates the `Requirement` status to "Feedback" and notifies the Engineer via a Celery task.
       - Given feedback, when the Engineer submits a PUT request to `/api/requirements/{req_id}/` with revised JSON, then MMS validates and updates the `Requirement` to status "Finalized".

2. **Fabrication**:
   - **Story**: As a Fabrication team member, I want to submit daily installation requirements for materials so that the Warehouse can prepare materials for widget fabrication.
     - **Acceptance Criteria**:
       - Given an authenticated Fabrication member, when they submit a POST request to `/api/installation_requirements/` with JSON `{ "material_id": "M123", "quantity": 50, "fab_date": "2025-06-15" }`, then MMS creates an `InstallationRequirement` instance and notifies Warehouse via a Celery task.
       - Given invalid JSON (e.g., non-existent `material_id`), when submitted, then MMS returns a 404 Not Found error.
   - **Story**: As a Fabrication team member, I want to receive finalized material specifications from Engineering so that I can plan widget fabrication accurately.
     - **Acceptance Criteria**:
       - Given a finalized `Requirement`, when MMS notifies Fabrication via a Celery task, then the specification is accessible via `GET /api/requirements/{req_id}/` with status "Finalized".

3. **Procurement**:
   - **Story**: As a Procurement officer, I want to review Engineering’s material requirements and provide feedback on availability and timing so that specifications are feasible.
     - **Acceptance Criteria**:
       - Given a new `Requirement`, when Procurement retrieves it via `GET /api/requirements/{req_id}/`, then they can submit feedback via `POST /api/requirements/{req_id}/feedback/`, updating the `Requirement` status to "Feedback".
       - Given no feedback within 24 hours, then MMS escalates to the Engineer via a Celery task.
   - **Story**: As a Procurement officer, I want to order materials based on finalized specifications so that Fabrication has what it needs on time.
     - **Acceptance Criteria**:
       - Given a finalized `Requirement`, when Procurement submits a POST request to `/api/materials/order/` with JSON `{ "req_id": "R123", "supplier_id": "S456" }`, then MMS creates a `Material` instance with status "Ordered".

4. **Sales**:
   - **Story**: As a Sales representative, I want to track material and widget availability so that I can inform customers about delivery timelines.
     - **Acceptance Criteria**:
       - Given authenticated Sales access, when querying `GET /api/materials/` or `GET /api/widgets/`, then MMS returns a list of instances with current availability and status.
       - Given a filtered query (e.g., `?status=Stored`), then MMS returns matching records.
   - **Story**: As a Sales representative, I want to receive customer receipt confirmations so that I can close sales orders.
     - **Acceptance Criteria**:
       - Given a shipped `CustomerOrder`, when the customer submits a POST request to `/api/orders/confirm/` with JSON `{ "order_id": "O123", "received": true }`, then MMS updates the order status to "Received".

5. **Warehouse**:
   - **Story**: As a Warehouse worker, I want to log material arrivals at the dock so that they can be processed for storage.
     - **Acceptance Criteria**:
       - Given authenticated Warehouse access, when submitting a POST request to `/api/materials/arrival/` with JSON `{ "shipment_id": "S123", "material_type": "steel", "quantity": 100 }`, then MMS creates a `Material` instance with status "Received" and assigns an inspection task via a Celery task.
       - Given incomplete JSON (e.g., missing `shipment_id`), then MMS returns a 400 Bad Request error.
   - **Story**: As a Warehouse worker, I want to fulfill material requisitions from Fabrication so that production can proceed.
     - **Acceptance Criteria**:
       - Given a Fabrication requisition, when submitting a POST request to `/api/materials/issue/` with JSON `{ "material_id": "M123", "quantity": 50 }`, then MMS updates the `Material` status to "Issued" and notifies Fabrication.

6. **Inventory**:
   - **Story**: As an Inventory manager, I want to locate materials for periodic inventory checks so that stock records are accurate.
     - **Acceptance Criteria**:
       - Given authenticated Inventory access, when querying `GET /api/inventory/`, then MMS returns a list of `InventoryRecord` instances with material IDs, locations, and last checked dates.
       - Given a specific `inv_id`, when querying `GET /api/inventory/{inv_id}/`, then MMS returns the corresponding record.
   - **Story**: As an Inventory manager, I want to update material statuses after inspections or maintenance so that the system reflects current conditions.
     - **Acceptance Criteria**:
       - Given an inspection or maintenance event, when submitting a PUT request to `/api/inventory/{inv_id}/` with JSON `{ "status": "Stored", "location": "Aisle 5" }`, then MMS updates the `InventoryRecord` and syncs with `Material`.

7. **Shipping**:
   - **Story**: As a Shipping coordinator, I want to prepare materials or widgets for shipping so that they reach customers on schedule.
     - **Acceptance Criteria**:
       - Given a ready `Material` or `Widget`, when submitting a POST request to `/api/shipments/` with JSON `{ "widget_id": "W123", "tracking_id": "T123" }`, then MMS creates a `Shipment` instance with status "Shipped".
       - Given insufficient stock, then MMS returns a 400 Bad Request error.
   - **Story**: As a Shipping coordinator, I want to log customer receipt confirmations so that delivery is documented.
     - **Acceptance Criteria**:
       - Given a shipped `Shipment`, when submitting a POST request to `/api/shipments/confirm/` with JSON `{ "shipment_id": "S123", "delivered": true }`, then MMS updates the status to "Delivered" and notifies Sales.

8. **Inspection**:
   - **Story**: As an Inspection officer, I want to perform quality inspections on arriving materials so that only compliant materials are stored.
     - **Acceptance Criteria**:
       - Given an assigned inspection task, when submitting a POST request to `/api/inspections/` with JSON `{ "material_id": "M123", "result": "Pass", "defects": null }`, then MMS creates an `Inspection` instance and updates `Material` status to "Stored".
       - Given incomplete JSON, then MMS returns a 400 Bad Request error.
   - **Story**: As an Inspection officer, I want to flag defective materials so that Procurement can address issues with suppliers.
     - **Acceptance Criteria**:
       - Given a failed inspection, when submitting a POST request to `/api/inspections/{inspection_id}/flag/` with JSON `{ "defects": "cracks detected" }`, then MMS notifies Procurement via a Celery task.

9. **Preventative Maintenance**:
   - **Story**: As a Preventative Maintenance technician, I want to schedule and perform maintenance on stored materials so that they remain usable.
     - **Acceptance Criteria**:
       - Given authenticated access, when submitting a POST request to `/api/maintenance/` with JSON `{ "material_id": "M123", "date": "2025-06-10" }`, then MMS creates a `MaintenanceRecord` instance and schedules a task via Celery.
       - Given a scheduling conflict, then MMS returns a 409 Conflict error.
   - **Story**: As a Preventative Maintenance technician, I want to update material conditions post-maintenance so that Inventory reflects their status.
     - **Acceptance Criteria**:
       - Given a completed maintenance task, when submitting a PUT request to `/api/maintenance/{maint_id}/` with JSON `{ "condition": "good" }`, then MMS updates the `MaintenanceRecord` and syncs `Material` status.

10. **Quality Control**:
    - **Story**: As a Quality Control officer, I want to verify widget quality post-fabrication so that only compliant widgets are shipped.
      - **Acceptance Criteria**:
        - Given a fabricated `Widget`, when submitting a POST request to `/api/inspections/` with JSON `{ "widget_id": "W123", "result": "Pass" }`, then MMS creates an `Inspection` instance and updates `Widget` status to "Ready for Shipping".
        - Given incomplete JSON, then MMS returns a 400 Bad Request error.
    - **Story**: As a Quality Control officer, I want to log quality issues for review so that Fabrication can improve processes.
      - **Acceptance Criteria**:
        - Given a failed widget inspection, when submitting a POST request to `/api/inspections/{inspection_id}/issues/` with JSON `{ "issues": "defective weld" }`, then MMS notifies Fabrication via a Celery task.

## Use Cases

Use Cases detail system interactions, incorporating Django-specific steps, edge cases, and Celery tasks for asynchronous processing.

### Use Case 1: Submit and Revise Material Requirements

- **Actors**: Engineer, Procurement
- **Precondition**: Engineer and Procurement are authenticated via DRF token authentication.
- **Description**: Engineer submits material requirements through the MMS API, triggering a Celery task for Procurement notification. Procurement reviews and provides feedback, which MMS processes and notifies Engineer. Engineer revises and finalizes specifications, stored as a `Requirement` model instance.
- **Steps**:
  1. Engineer submits a POST request to `/api/requirements/` with JSON payload `{ "material_type": "steel", "quantity": 100, "delivery_date": "2025-06-01" }`.
  2. DRF validates the payload using `RequirementSerializer`, creates a `Requirement` instance (status: "Draft"), and queues a Celery task (`notify_procurement_task`) to alert Procurement.
  3. Procurement retrieves the requirement via `GET /api/requirements/{req_id}/` and submits feedback via `POST /api/requirements/{req_id}/feedback/` with JSON `{ "availability": "limited", "lead_time": "2 weeks" }`.
  4. MMS updates the `Requirement` status to "Feedback" and queues a Celery task (`notify_engineer_task`) to alert Engineer.
  5. Engineer revises specifications via `PUT /api/requirements/{req_id}/` with updated JSON `{ "quantity": 80, "delivery_date": "2025-06-15" }`.
  6. DRF validates using `RequirementSerializer`, updates the `Requirement` to status "Finalized", and queues a Celery task (`notify_fabrication_task`) to alert Fabrication.
- **Postcondition**: Finalized `Requirement` is stored in `mms.db`, accessible to Fabrication via `GET /api/requirements/`.
- **Exceptions**:
  - If feedback is delayed beyond 24 hours, MMS triggers a Celery task (`escalate_delay_task`) to send an escalation email to Engineer.
  - If the payload is invalid (e.g., negative quantity), DRF returns a 400 Bad Request error with validation details.
- **Edge Cases**:
  - Multiple feedback iterations: MMS allows up to three revisions, then escalates to a manager via a Celery task.
  - Unauthorized access: DRF returns a 401 Unauthorized error for non-authenticated users.
  - Network failure during notification: Celery retries the task up to three times.
- **UML Reference**:
  - Activity Diagram:  
    ![Activity Diagram](../artifacts/Activity_Diagram_r1.png)  
    [Link to Activity Diagram](../artifacts/Activity_Diagram_r1.png)
  - Sequence Diagram:  
    ![Sequence Diagram](../artifacts/Sequence_Diagram_r1.png)  
    [Link to Sequence Diagram](../artifacts/Sequence_Diagram_r1.png)
  - Use Case Diagram:  
    ![Use Case Diagram](../artifacts/Use_Case_Diagram_r1.png)  
    [Link to Use Case Diagram](../artifacts/Use_Case_Diagram_r1.png)

### Use Case 2: Process Material Arrival and Inspection

- **Actors**: Warehouse, Inspection
- **Precondition**: Material shipment arrives at the dock; Warehouse and Inspection officers are authenticated via DRF.
- **Description**: Warehouse logs material arrival through the API, triggering an inspection task via Celery. The Inspection officer logs results, updating the `Material` model status, with notifications handled by Celery tasks.
- **Steps**:
  1. Warehouse worker submits a POST request to `/api/materials/arrival/` with JSON `{ "shipment_id": "S123", "material_type": "steel", "quantity": 100 }`.
  2. DRF validates using `MaterialSerializer`, creates a `Material` instance with status "Received", and queues a Celery task (`assign_inspection_task`) to notify Inspection.
  3. Inspection officer retrieves tasks via `GET /api/inspections/` and submits results via `POST /api/inspections/` with JSON `{ "material_id": "M123", "result": "Pass", "defects": null }`.
  4. MMS creates an `Inspection` instance; if passed, updates `Material` status to "Stored" and notifies Warehouse via a Celery task (`notify_warehouse_task`); if failed, updates to "Flagged" and notifies Procurement.
  5. Warehouse submits a POST request to `/api/materials/{material_id}/store/` with JSON `{ "location": "Aisle 5" }` to update the `InventoryRecord`.
- **Postcondition**: `Material` is stored or flagged in `mms.db`, with an updated `InventoryRecord` if stored.
- **Exceptions**:
  - If inspection fails, MMS halts storage and notifies Procurement via a Celery task (`notify_procurement_task`).
  - If arrival data is incomplete (e.g., missing `shipment_id`), DRF returns a 400 Bad Request error.
- **Edge Cases**:
  - Partial shipment: MMS logs partial quantities and flags for Procurement review via a Celery task.
  - Inspection delay (>12 hours): MMS escalates to Inspection manager via a Celery task.
  - Duplicate shipment ID: MMS returns a 409 Conflict error.
- **UML Reference**:
  - State Machine Diagram:  
    ![State Machine Diagram](../artifacts/State_Machine_Diagram_r1.png)  
    [Link to State Machine Diagram](../artifacts/State_Machine_Diagram_r1.png)
  - Use Case Diagram:  
    ![Use Case Diagram](../artifacts/Use_Case_Diagram_r1.png)  
    [Link to Use Case Diagram](../artifacts/Use_Case_Diagram_r1.png)

### Use Case 3: Fabricate Widgets and Ship to Customer

- **Actors**: Fabrication, Quality Control, Shipping, Sales
- **Precondition**: Finalized material specifications are stored in MMS; materials are in storage; actors are authenticated.
- **Description**: Fabrication requisitions materials, fabricates widgets, Quality Control verifies quality, and Shipping delivers to the customer, with Sales logging receipt. All interactions occur via API endpoints, with Celery tasks for notifications and model updates.
- **Steps**:
  1. Fabrication submits a POST request to `/api/installation_requirements/` with JSON `{ "material_id": "M123", "quantity": 50, "fab_date": "2025-06-15" }` and a POST to `/api/materials/issue/` with `{ "material_id": "M123", "quantity": 50 }`.
  2. DRF validates using `MaterialSerializer`, updates `Material` status to "Issued", and queues a Celery task (`notify_warehouse_task`) to alert Warehouse.
  3. Fabrication fabricates widgets and submits a POST request to `/api/widgets/` with JSON `{ "material_id": "M123", "status": "Fabricated" }`.
  4. Quality Control submits a POST request to `/api/inspections/` with JSON `{ "widget_id": "W123", "result": "Pass" }`.
  5. MMS creates an `Inspection` instance; if passed, updates `Widget` status to "Ready for Shipping" and notifies Shipping via a Celery task (`notify_shipping_task`).
  6. Shipping submits a POST request to `/api/shipments/` with JSON `{ "widget_id": "W123", "tracking_id": "T123", "customer_id": "C456" }`, updating `Shipment` status to "Shipped".
  7. Sales submits a POST request to `/api/orders/confirm/` with JSON `{ "order_id": "O123", "received": true }`, updating `CustomerOrder` status to "Received".
- **Postcondition**: `Widget` is delivered, and receipt is recorded in `mms.db` as a `CustomerOrder`.
- **Exceptions**:
  - If quality check fails, MMS notifies Fabrication for rework via a Celery task (`notify_fabrication_task`).
  - If shipping is delayed (>24 hours), MMS escalates to Sales via a Celery task (`escalate_shipping_task`).
- **Edge Cases**:
  - Partial widget batch: MMS allows partial shipping, logging a note in the `Shipment` record.
  - Customer rejection: MMS reverts `CustomerOrder` status to "Shipped" and notifies Sales via a Celery task.
  - Insufficient material quantity: MMS returns a 400 Bad Request error during requisition.
- **UML Reference**:
  - State Machine Diagram:  
    ![State Machine Diagram](../artifacts/State_Machine_Diagram_r1.png)  
    [Link to State Machine Diagram](../artifacts/State_Machine_Diagram_r1.png)
  - Use Case Diagram:  
    ![Use Case Diagram](../artifacts/Use_Case_Diagram_r1.png)  
    [Link to Use Case Diagram](../artifacts/Use_Case_Diagram_r1.png)

## UML Diagrams

The MMS UML diagrams are stored in the `artifacts` folder at the project root. All Evolution 1 diagrams are suffixed with `_r1` to distinguish from Evolution 0 diagrams, which remain available in `Evolution_0/requirements.md`. Evolution 1 updates include Django-specific details (e.g., model fields, API endpoints, view interactions) for the Activity, Class, and Sequence Diagrams, while Component, State Machine, and Use Case Diagrams have been renamed with `_r1` for consistency.

- **Activity Diagram**:  
  ![Activity Diagram](../artifacts/Activity_Diagram_r1.png)  
  [Link to Activity Diagram](../artifacts/Activity_Diagram_r1.png)

- **Class Diagram**:  
  ![Class Diagram](../artifacts/Class_Diagram_r1.png)  
  [Link to Class Diagram](../artifacts/Class_Diagram_r1.png)

- **Component Diagram**:  
  ![Component Diagram](../artifacts/Component_Diagram_r1.png)  
  [Link to Component Diagram](../artifacts/Component_Diagram_r1.png)

- **Sequence Diagram**:  
  ![Sequence Diagram](../artifacts/Sequence_Diagram_r1.png)  
  [Link to Sequence Diagram](../artifacts/Sequence_Diagram_r1.png)

- **State Machine Diagram**:  
  ![State Machine Diagram](../artifacts/State_Machine_Diagram_r1.png)  
  [Link to State Machine Diagram](../artifacts/State_Machine_Diagram_r1.png)

- **Use Case Diagram**:  
  ![Use Case Diagram](../artifacts/Use_Case_Diagram_r1.png)  
  [Link to Use Case Diagram](../artifacts/Use_Case_Diagram_r1.png)

## System Overview

The MMS integrates data from disparate systems (Engineering, Procurement, Fabrication, etc.) without replacing their Systems of Record. It uses a low-code/no-code platform for data feeds, ETL transformations, and analytics. Built with DRF, Django ORM, and SQLite (`mms.db`), it supports CRUD endpoints (`/api/materials/`, `/api/requirements/`) and beyond-CRUD operations (reports, notifications, progress tracking). Celery with Redis in Docker handles asynchronous tasks, such as notifications and report generation, ensuring scalability. Unit tests will validate functionality in future evolutions. The Django admin UI at `http://localhost:8000/admin/` provides a user-friendly interface for all personas.

## Next Steps

- **Evolution 2**: Design the DRF API and ERD for MMS entities (`Material`, `Requirement`, `Widget`, etc.).
- **Evolution 4**: Implement Django models, views, and URLs in `mms/apps/`.
- **Evolution 5**: Develop a Ubiquitous Language Glossary, Gherkin Notation for the three Use Cases, and Django unittests to validate system functionality.
