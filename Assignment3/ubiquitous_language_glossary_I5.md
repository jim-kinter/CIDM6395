# Ubiquitous Language Glossary

This glossary defines key terms used in the Materials Management System (MMS) to ensure consistent understanding across stakeholders, developers, and documentation in the domain of industrial manufacturing material management.

- **Material**: A raw resource (e.g., steel, aluminum) tracked from arrival to issuance for fabrication. Represented by the `Material` model with attributes like `type`, `quantity`, and `status`.
- **Requirement**: A demand for materials submitted by Engineering, subject to feedback from Procurement. Represented by the `Requirement` model with attributes like `quantity`, `delivery_date`, and `status` (Draft, Feedback, Finalized).
- **Installation Requirement**: A specific material need for widget production, requested by Fabrication. Represented by the `InstallationRequirement` model with attributes like `quantity` and `fab_date`.
- **Widget**: A fabricated product made from materials, ready for inspection and shipping. Represented by the `Widget` model with attributes like `status` (Fabricated, Inspected, Shipped).
- **Shipment**: A delivery of materials or widgets to customers, tracked from preparation to delivery. Represented by the `Shipment` model with attributes like `tracking_id`, `customer_id`, and `status` (Prepared, Shipped, Delivered).
- **Inspection**: A quality check on materials or widgets, determining if they pass or fail. Represented by the `Inspection` model with attributes like `result` (Pass, Fail) and `defects`.
- **Maintenance Record**: A record of maintenance activities on stored materials. Represented by the `MaintenanceRecord` model with attributes like `date` and `condition`.
- **Inventory Record**: A tracking entry for materials in inventory, including location and last checked date. Represented by the `InventoryRecord` model with attributes like `location` and `last_checked`.
- **Customer Order**: An order placed by a customer for materials or widgets, tracked until receipt. Represented by the `CustomerOrder` model with attributes like `customer_id` and `status`.
- **Engineer**: A persona responsible for submitting and revising material requirements.
- **Procurement**: A persona providing feedback on material requirements (e.g., availability, lead time).
- **Fabrication**: A persona responsible for producing widgets from materials.
- **Warehouse**: A persona managing material storage and inventory.
- **Shipping**: A persona handling the shipment of widgets to customers.
- **Material Demand Report**: A report aggregating material requirements and installation requirements over a date range, generated asynchronously via Celery.
- **Notification**: An asynchronous message sent to personas (e.g., "Material flagged with defects"), handled via Celery tasks.
