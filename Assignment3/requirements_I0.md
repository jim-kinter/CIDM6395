# MMS Requirements Specification

## Overview

The Materials Management System (MMS) is a Django REST Framework (DRF) application designed to manage material demand in industrial manufacturing. It integrates daily material requirements from Engineering and installation requirements from Fabrication, with a feedback loop between Procurement and Engineering to finalize specifications. The system tracks materials from dock arrival through receiving, quality inspection, storage, preventative maintenance, requisition, inventory, widget fabrication, shipping, and customer delivery. Key personas include Engineer, Fabrication, Procurement, Sales, Warehouse, Inventory, Shipping, Inspection, Preventative Maintenance, and Quality Control. The MMS uses SQLite (`mms.db`), Celery with Redis in Docker for asynchronous tasks, and provides a Django admin UI at `http://localhost:8000/admin/`. UML diagrams (PNG files) are located in the `artifacts` folder at the project root, rendered from PlantUML at `https://plantuml.online`.

## User Stories

User Stories capture the needs of each persona, following the format: **As a [persona], I want to [action] so that [benefit]**.

1. **Engineer**:
   - As an Engineer, I want to submit daily material requirements so that Procurement can order the correct materials.
   - As an Engineer, I want to receive Procurement feedback on material availability and timing so that I can revise and finalize specifications.

2. **Fabrication**:
   - As a Fabrication team member, I want to submit daily installation requirements for materials so that the Warehouse can prepare materials for widget fabrication.
   - As a Fabrication team member, I want to receive finalized material specifications from Engineering so that I can plan widget fabrication accurately.

3. **Procurement**:
   - As a Procurement officer, I want to review Engineering’s material requirements and provide feedback on availability and timing so that specifications are feasible.
   - As a Procurement officer, I want to order materials based on finalized specifications so that Fabrication has what it needs on time.

4. **Sales**:
   - As a Sales representative, I want to track material and widget availability so that I can inform customers about delivery timelines.
   - As a Sales representative, I want to receive customer receipt confirmations so that I can close sales orders.

5. **Warehouse**:
   - As a Warehouse worker, I want to log material arrivals at the dock so that they can be processed for storage.
   - As a Warehouse worker, I want to fulfill material requisitions from Fabrication so that production can proceed.

6. **Inventory**:
   - As an Inventory manager, I want to locate materials for periodic inventory checks so that stock records are accurate.
   - As an Inventory manager, I want to update material statuses after inspections or maintenance so that the system reflects current conditions.

7. **Shipping**:
   - As a Shipping coordinator, I want to prepare materials or widgets for shipping so that they reach customers on schedule.
   - As a Shipping coordinator, I want to log customer receipt confirmations so that delivery is documented.

8. **Inspection**:
   - As an Inspection officer, I want to perform quality inspections on arriving materials so that only compliant materials are stored.
   - As an Inspection officer, I want to flag defective materials so that Procurement can address issues with suppliers.

9. **Preventative Maintenance**:
   - As a Preventative Maintenance technician, I want to schedule and perform maintenance on stored materials so that they remain usable.
   - As a Preventative Maintenance technician, I want to update material conditions post-maintenance so that Inventory reflects their status.

10. **Quality Control**:
    - As a Quality Control officer, I want to verify widget quality post-fabrication so that only compliant widgets are shipped.
    - As a Quality Control officer, I want to log quality issues for review so that Fabrication can improve processes.

## Use Cases

Use Cases detail key system interactions, specifying actors, preconditions, steps, and postconditions.

### Use Case 1: Submit and Revise Material Requirements

- **Actors**: Engineer, Procurement
- **Precondition**: Engineer has access to MMS; Procurement is ready to review.
- **Description**: Engineer submits daily material requirements. Procurement reviews and provides feedback. Engineer revises and finalizes specifications.
- **Steps**:
  1. Engineer logs into MMS and submits material requirements (e.g., material type, quantity, delivery date).
  2. MMS notifies Procurement of new requirements.
  3. Procurement reviews and inputs feedback (e.g., availability, lead times).
  4. Engineer receives feedback via MMS and revises specifications.
  5. Engineer submits finalized requirements.
  6. MMS stores finalized specifications and notifies Fabrication.
- **Postcondition**: Finalized requirements are stored and accessible to Fabrication.
- **Exceptions**:
  - If feedback is delayed, MMS escalates to Engineer.
  - If specifications are invalid, MMS prompts Engineer for corrections.
- **UML Reference**:
  - Activity Diagram:  
    ![Activity Diagram](../artifacts/Activity_Diagram.png)  
    [Link to Activity Diagram](../artifacts/Activity_Diagram.png)
  - Sequence Diagram:  
    ![Sequence Diagram](../artifacts/Sequence_Diagram.png)  
    [Link to Sequence Diagram](../artifacts/Sequence_Diagram.png)
  - Use Case Diagram:  
    ![Use Case Diagram](../artifacts/Use_Case_Diagram.png)  
    [Link to Use Case Diagram](../artifacts/Use_Case_Diagram.png)

### Use Case 2: Process Material Arrival and Inspection

- **Actors**: Warehouse, Inspection
- **Precondition**: Material shipment arrives at the dock; Inspection is scheduled.
- **Description**: Warehouse logs material arrival, and Inspection performs quality checks before storage.
- **Steps**:
  1. Warehouse worker logs into MMS and records material arrival (e.g., shipment ID, material type, quantity).
  2. MMS assigns an inspection task to Inspection officer.
  3. Inspection officer performs quality check and logs results (pass/fail, defects).
  4. If passed, MMS updates material status to "ready for storage" and notifies Warehouse.
  5. Warehouse moves materials to storage and updates location in MMS.
  6. If failed, MMS flags defects and notifies Procurement.
- **Postcondition**: Materials are stored or flagged for Procurement action.
- **Exceptions**:
  - If inspection fails, MMS halts storage and escalates to Procurement.
  - If arrival data is incomplete, MMS prompts Warehouse for corrections.
- **UML Reference**:
  - State Machine Diagram:  
    ![State Machine Diagram](../artifacts/State_Machine_Diagram.png)  
    [Link to State Machine Diagram](../artifacts/State_Machine_Diagram.png)
  - Use Case Diagram:  
    ![Use Case Diagram](../artifacts/Use_Case_Diagram.png)  
    [Link to Use Case Diagram](../artifacts/Use_Case_Diagram.png)

### Use Case 3: Fabricate Widgets and Ship to Customer

- **Actors**: Fabrication, Quality Control, Shipping, Sales
- **Precondition**: Finalized material specifications are available; materials are in storage.
- **Description**: Fabrication requisitions materials, fabricates widgets, Quality Control verifies quality, and Shipping delivers to the customer.
- **Steps**:
  1. Fabrication submits installation requirements and material requisition via MMS.
  2. Warehouse fulfills requisition, updating material status to "issued".
  3. Fabrication fabricates widgets and logs completion in MMS.
  4. Quality Control performs inspection and logs results (pass/fail).
  5. If passed, MMS updates widget status to "ready for shipping" and notifies Shipping.
  6. Shipping prepares and ships widgets, logging tracking details.
  7. Customer confirms receipt, and Sales logs confirmation in MMS.
- **Postcondition**: Widgets are delivered, and receipt is recorded.
- **Exceptions**:
  - If quality check fails, MMS notifies Fabrication for rework.
  - If shipping is delayed, MMS escalates to Sales.
- **UML Reference**:
  - State Machine Diagram:  
    ![State Machine Diagram](../artifacts/State_Machine_Diagram.png)  
    [Link to State Machine Diagram](../artifacts/State_Machine_Diagram.png)
  - Use Case Diagram:  
    ![Use Case Diagram](../artifacts/Use_Case_Diagram.png)  
    [Link to Use Case Diagram](../artifacts/Use_Case_Diagram.png)

## UML Diagrams

The MMS UML diagrams, rendered as PNG files from PlantUML at `https://plantuml.online`, are stored in the `artifacts` folder at the project root. Below are the diagrams with inline images and links:

- **Activity Diagram**:  
  ![Activity Diagram](../artifacts/Activity_Diagram.png)  
  [Link to Activity Diagram](../artifacts/Activity_Diagram.png)

- **Class Diagram**:  
  ![Class Diagram](../artifacts/Class_Diagram.png)  
  [Link to Class Diagram](../artifacts/Class_Diagram.png)

- **Component Diagram**:  
  ![Component Diagram](../artifacts/Component_Diagram.png)  
  [Link to Component Diagram](../artifacts/Component_Diagram.png)

- **Sequence Diagram**:  
  ![Sequence Diagram](../artifacts/Sequence_Diagram.png)  
  [Link to Sequence Diagram](../artifacts/Sequence_Diagram.png)

- **State Machine Diagram**:  
  ![State Machine Diagram](../artifacts/State_Machine_Diagram.png)  
  [Link to State Machine Diagram](../artifacts/State_Machine_Diagram.png)

- **Use Case Diagram**:  
  ![Use Case Diagram](../artifacts/Use_Case_Diagram.png)  
  [Link to Use Case Diagram](../artifacts/Use_Case_Diagram.png)

## System Overview

The MMS integrates data from disparate systems (Engineering, Procurement, Fabrication, etc.) without replacing their Systems of Record. It uses a low-code/no-code platform for data feeds, ETL transformations, and analytics. Built with DRF, Django ORM, and SQLite (`mms.db`), it supports CRUD endpoints (`/materials/`, `/requirements/`) and beyond-CRUD operations (reports, notifications, progress tracking). Celery with Redis in Docker handles asynchronous tasks, and unit tests validate functionality. The admin UI enables data management.

## Next Steps

- **Evolution 1**: Refine User Stories with acceptance criteria and update UML diagrams with Django specifics.
- **Evolution 2**: Design DRF API and ERD for MMS entities.
- **Evolution 4**: Implement Django models, views, and URLs.
- **Evolution 5**: Develop Ubiquitous Language Glossary, Gherkin Notation, and unittests for three Use Cases.
