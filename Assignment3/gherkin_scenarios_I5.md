# Gherkin Scenarios for MMS Entities and Use Cases

This document defines Gherkin scenarios for testing each entity in the Materials Management System (MMS) and the three previously defined Use Cases, using Given/When/Then syntax to specify acceptance criteria.

## Entity Tests

### Material

**Feature**: Material Management  
As a Warehouse staff member, I want to manage materials through their lifecycle, from arrival to issuance, to ensure availability for fabrication.

**Scenario**: Create a Material via Arrival  
Given a Warehouse staff member is authenticated  
When the staff submits a POST request to "/api/materials/arrival/" with payload {"shipment_id": "S123", "material_type": "steel", "quantity": 100}  
Then the response status is 201 Created  
And the response contains a material with "status": "Received"  
And a Celery task notifies the Warehouse with "Inspection task assigned for material arrival"

**Scenario**: Update Material Storage Location  
Given a Material with ID "<material_id>" exists with status "Received"  
And a Warehouse staff member is authenticated  
When the staff submits a PUT request to "/api/materials/<material_id>/store/" with payload {"location": "Aisle 5"}  
Then the response status is 200 OK  
And the material’s "status" is updated to "Stored"  
And the material’s location is "Aisle 5"

**Scenario**: Issue Material for Fabrication  
Given a Material with ID "<material_id>" exists with quantity 100 and status "Stored"  
And Fabrication is authenticated  
When Fabrication submits a POST request to "/api/materials/issue/" with payload {"material_id": "<material_id>", "quantity": 50}  
Then the response status is 200 OK  
And the material’s "status" is updated to "Issued"  
And the material’s quantity is updated to 50  
And a Celery task notifies Fabrication with "Material <material_id> issued for fabrication"

**Scenario**: Delete a Material  
Given a Material with ID "<material_id>" exists  
And an admin user is authenticated  
When the admin submits a DELETE request to "/api/materials/<material_id>/"  
Then the response status is 204 No Content  
And the material is removed from the database

**Scenario**: Generate Material Demand Report  
Given a Warehouse staff member is authenticated  
When the staff submits a POST request to "/api/materials/report/" with payload {"start_date": "2025-06-01", "end_date": "2025-06-30"}  
Then the response status is 200 OK  
And the response contains a "report_id" and "status": "Generating"  
And a Celery task is triggered to generate the report

### Requirement

**Feature**: Requirement Management  
As an Engineer, I want to submit and revise material requirements, so that material demands are accurately specified.

**Scenario**: Submit a Material Requirement  
Given an Engineer is authenticated  
When the Engineer submits a POST request to "/api/requirements/" with payload {"material_type": "steel", "quantity": 100, "delivery_date": "2025-06-01"}  
Then the response status is 201 Created  
And the response contains a requirement with "status": "Draft"  
And a Celery task notifies Procurement with "New requirement <req_id> created"

**Scenario**: Provide Feedback on a Requirement  
Given a Requirement with ID "<req_id>" exists with status "Draft"  
And Procurement is authenticated  
When Procurement submits a POST request to "/api/requirements/<req_id>/feedback/" with payload {"availability": "limited", "lead_time": "2 weeks"}  
Then the response status is 200 OK  
And the requirement’s "status" is updated to "Feedback"  
And a Celery task notifies the Engineer with "Feedback received for requirement <req_id>"

**Scenario**: Finalize a Requirement  
Given a Requirement with ID "<req_id>" exists with status "Feedback"  
And the Engineer is authenticated  
When the Engineer submits a PUT request to "/api/requirements/<req_id>/" with payload {"quantity": 80, "delivery_date": "2025-06-15"}  
Then the response status is 200 OK  
And the requirement’s "status" is updated to "Finalized"  
And a Celery task notifies Fabrication with "Requirement <req_id> finalized"

### InstallationRequirement

**Feature**: Installation Requirement Management  
As a Fabrication staff member, I want to request materials for widget production, so that production can proceed.

**Scenario**: Submit an Installation Requirement  
Given Fabrication is authenticated  
And a Material with ID "<material_id>" exists  
When Fabrication submits a POST request to "/api/installation_requirements/" with payload {"material_id": "<material_id>", "quantity": 50, "fab_date": "2025-06-15"}  
Then the response status is 201 Created  
And the response contains an installation requirement  
And a Celery task notifies the Warehouse with "Installation requirement <inst_req_id> created for fabrication"

**Scenario**: Update an Installation Requirement  
Given an Installation Requirement with ID "<inst_req_id>" exists  
And Fabrication is authenticated  
When Fabrication submits a PUT request to "/api/installation_requirements/<inst_req_id>/" with payload {"quantity": 60, "fab_date": "2025-06-16"}  
Then the response status is 200 OK  
And the installation requirement’s quantity is updated to 60

### Widget

**Feature**: Widget Management  
As a Fabrication staff member, I want to manage widgets through their lifecycle, from fabrication to shipping readiness.

**Scenario**: Create a Widget  
Given a Material with ID "<material_id>" exists with status "Issued"  
And Fabrication is authenticated  
When Fabrication submits a POST request to "/api/widgets/" with payload {"material_id": "<material_id>", "status": "Fabricated"}  
Then the response status is 201 Created  
And the response contains a widget with "status": "Fabricated"

**Scenario**: Update Widget Status After Inspection  
Given a Widget with ID "<widget_id>" exists with status "Fabricated"  
And Fabrication is authenticated  
When Fabrication submits a PUT request to "/api/widgets/<widget_id>/" with payload {"status": "Inspected"}  
Then the response status is 200 OK  
And the widget’s "status" is updated to "Inspected"

### Shipment

**Feature**: Shipment Management  
As a Shipping staff member, I want to manage shipments to customers, ensuring delivery confirmation.

**Scenario**: Prepare a Shipment  
Given a Widget with ID "<widget_id>" exists with status "Inspected"  
And Shipping is authenticated  
When Shipping submits a POST request to "/api/shipments/" with payload {"widget_id": "<widget_id>", "tracking_id": "T123", "customer_id": "C456"}  
Then the response status is 201 Created  
And the response contains a shipment with "status": "Shipped"  
And a Celery task notifies Shipping with "Shipment <shipment_id> prepared"

**Scenario**: Confirm Shipment Delivery  
Given a Shipment with ID "<shipment_id>" exists with status "Shipped"  
And Shipping is authenticated  
When Shipping submits a POST request to "/api/shipments/confirm/" with payload {"shipment_id": "<shipment_id>", "delivered": true}  
Then the response status is 200 OK  
And the shipment’s "status" is updated to "Delivered"  
And a Celery task notifies Shipping with "Shipment <shipment_id> delivered"

### Inspection

**Feature**: Inspection Management  
As an Inspector, I want to perform inspections on materials and widgets, ensuring quality control.

**Scenario**: Perform Material Inspection (Pass)  
Given a Material with ID "<material_id>" exists with status "Received"  
And an Inspector is authenticated  
When the Inspector submits a POST request to "/api/inspections/" with payload {"material_id": "<material_id>", "result": "Pass", "defects": null}  
Then the response status is 201 Created  
And the material’s "status" is updated to "Stored"  
And a Celery task notifies the Warehouse with "Inspection <inspection_id> completed for material"

**Scenario**: Flag Material for Defects  
Given an Inspection with ID "<inspection_id>" exists for a Material  
And the Inspector is authenticated  
When the Inspector submits a POST request to "/api/inspections/<inspection_id>/flag/" with payload {"defects": "cracks detected"}  
Then the response status is 200 OK  
And a Celery task notifies Procurement with "Material flagged with defects: cracks detected"

### MaintenanceRecord

**Feature**: Maintenance Record Management  
As a Warehouse staff member, I want to record maintenance activities on stored materials, ensuring material quality.

**Scenario**: Schedule a Maintenance Task  
Given a Material with ID "<material_id>" exists with status "Stored"  
And a Warehouse staff member is authenticated  
When the staff submits a POST request to "/api/maintenance/" with payload {"material_id": "<material_id>", "date": "2025-06-10"}  
Then the response status is 201 Created  
And the response contains a maintenance record

**Scenario**: Update Maintenance Condition  
Given a Maintenance Record with ID "<maint_id>" exists  
And a Warehouse staff member is authenticated  
When the staff submits a PUT request to "/api/maintenance/<maint_id>/" with payload {"condition": "good"}  
Then the response status is 200 OK  
And the maintenance record’s condition is updated to "good"

### InventoryRecord

**Feature**: Inventory Record Management  
As a Warehouse staff member, I want to track material inventory, ensuring accurate stock management.

**Scenario**: Create an Inventory Record  
Given a Material with ID "<material_id>" exists with status "Stored"  
And a Warehouse staff member is authenticated  
When the staff submits a POST request to "/api/inventory/" with payload {"material_id": "<material_id>", "location": "Aisle 5", "last_checked": "2025-06-01"}  
Then the response status is 201 Created  
And the response contains an inventory record

**Scenario**: Update Inventory Location  
Given an Inventory Record with ID "<inv_id>" exists  
And a Warehouse staff member is authenticated  
When the staff submits a PUT request to "/api/inventory/<inv_id>/" with payload {"location": "Aisle 6"}  
Then the response status is 200 OK  
And the inventory record’s location is updated to "Aisle 6"

### CustomerOrder

**Feature**: Customer Order Management  
As a Shipping staff member, I want to manage customer orders, ensuring timely delivery and confirmation.

**Scenario**: Create a Customer Order  
Given a Widget with ID "<widget_id>" exists with status "Inspected"  
And Shipping is authenticated  
When Shipping submits a POST request to "/api/orders/" with payload {"widget_id": "<widget_id>", "customer_id": "C789", "status": "Pending"}  
Then the response status is 201 Created  
And the response contains a customer order with "status": "Pending"

**Scenario**: Confirm Customer Order Receipt  
Given a Customer Order with ID "<order_id>" exists with status "Shipped"  
And Shipping is authenticated  
When Shipping submits a POST request to "/api/orders/confirm/" with payload {"order_id": "<order_id>", "received": true}  
Then the response status is 200 OK  
And the order’s "status" is updated to "Received"

**Scenario**: Calculate Order Progress  
Given a Customer Order with ID "<order_id>" exists with status "Shipped"  
And Shipping is authenticated  
When Shipping submits a GET request to "/api/orders/<order_id>/progress/"  
Then the response status is 200 OK  
And the response contains "progress_percentage": 75 and "status": "Shipped"

## Use Case Tests

### Use Case 1: Submit and Revise Material Requirements

**Scenario**: Engineer Submits a Material Requirement  
Given an Engineer is authenticated  
When the Engineer submits a POST request to "/api/requirements/" with payload {"material_type": "steel", "quantity": 100, "delivery_date": "2025-06-01"}  
Then the response status is 201 Created  
And the response contains a requirement with "status": "Draft"  
And a Celery task notifies Procurement with "New requirement <req_id> created"

**Scenario**: Procurement Provides Feedback on a Requirement  
Given a Requirement with ID "<req_id>" exists with status "Draft"  
And Procurement is authenticated  
When Procurement submits a POST request to "/api/requirements/<req_id>/feedback/" with payload {"availability": "limited", "lead_time": "2 weeks"}  
Then the response status is 200 OK  
And the requirement’s "status" is updated to "Feedback"  
And a Celery task notifies the Engineer with "Feedback received for requirement <req_id>"

**Scenario**: Engineer Revises and Finalizes a Requirement  
Given a Requirement with ID "<req_id>" exists with status "Feedback"  
And the Engineer is authenticated  
When the Engineer submits a PUT request to "/api/requirements/<req_id>/" with payload {"quantity": 80, "delivery_date": "2025-06-15"}  
Then the response status is 200 OK  
And the requirement’s "status" is updated to "Finalized"  
And a Celery task notifies Fabrication with "Requirement <req_id> finalized"

### Use Case 2: Process Material Arrival and Inspection

**Scenario**: Warehouse Logs Material Arrival  
Given a Warehouse staff member is authenticated  
When the staff submits a POST request to "/api/materials/arrival/" with payload {"shipment_id": "S123", "material_type": "steel", "quantity": 100}  
Then the response status is 201 Created  
And the response contains a material with "status": "Received"  
And a Celery task notifies the Warehouse with "Inspection task assigned for material arrival"

**Scenario**: Warehouse Performs Material Inspection  
Given a Material with ID "<material_id>" exists with status "Received"  
And an Inspector is authenticated  
When the Inspector submits a POST request to "/api/inspections/" with payload {"material_id": "<material_id>", "result": "Pass", "defects": null}  
Then the response status is 201 Created  
And the material’s "status" is updated to "Stored"  
And a Celery task notifies the Warehouse with "Inspection <inspection_id> completed for material"

**Scenario**: Inspector Flags a Material for Defects  
Given an Inspection with ID "<inspection_id>" exists for a Material  
And the Inspector is authenticated  
When the Inspector submits a POST request to "/api/inspections/<inspection_id>/flag/" with payload {"defects": "cracks detected"}  
Then the response status is 200 OK  
And a Celery task notifies Procurement with "Material flagged with defects: cracks detected"

### Use Case 3: Fabricate Widgets and Ship to Customer

**Scenario**: Fabrication Issues Materials for Widget Production  
Given a Material with ID "<material_id>" exists with quantity 100 and status "Stored"  
And Fabrication is authenticated  
When Fabrication submits a POST request to "/api/materials/issue/" with payload {"material_id": "<material_id>", "quantity": 50}  
Then the response status is 200 OK  
And the material’s "status" is updated to "Issued"  
And the material’s quantity is updated to 50  
And a Celery task notifies Fabrication with "Material <material_id> issued for fabrication"

**Scenario**: Fabrication Creates a Widget  
Given a Material with ID "<material_id>" exists with status "Issued"  
And Fabrication is authenticated  
When Fabrication submits a POST request to "/api/widgets/" with payload {"material_id": "<material_id>", "status": "Fabricated"}  
Then the response status is 201 Created  
And the response contains a widget with "status": "Fabricated"

**Scenario**: Shipping Confirms Delivery to Customer  
Given a Shipment with ID "<shipment_id>" exists with status "Shipped"  
And Shipping is authenticated  
When Shipping submits a POST request to "/api/shipments/confirm/" with payload {"shipment_id": "<shipment_id>", "delivered": true}  
Then the response status is 200 OK  
And the shipment’s "status" is updated to "Delivered"  
And a Celery task notifies Shipping with "Shipment <shipment_id> delivered"
