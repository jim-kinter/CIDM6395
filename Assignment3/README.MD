# CIDM6330-Spring2025

Repository for CIDM6330

## PROBLEM DESCRIPTION

Materials management in industrial manufacturing is a complex, high-stakes process involving millions of materials, global supply chains, and intricate coordination across Engineering, Procurement, and Fabrication. The system must handle daily material requirements from Engineering, installation schedules from Fabrication (lagging by up to a month due to Procurement-Engineering feedback loops), and track materials through receiving, inspection, storage, maintenance, requisition, inventory, shipping, and customer delivery. These processes are managed across disparate systems, leading to fragmented data, manual reconciliations, and delays. Challenges include ensuring material availability, meeting quality standards, maintaining inventory accuracy, and aligning with customer delivery timelines, all while managing regulatory, logistical, and quality constraints. Without integrated visibility, errors, inefficiencies, and missed deadlines create significant financial and operational risks.

## DOMAIN

Materials Management in industrial manufacturing, encompassing Engineering (material requirements), Procurement (ordering and feedback), Fabrication (widget production), and logistics (receiving, inspection, storage, maintenance, inventory, shipping, quality control). Key sub-disciplines include demand planning, supply chain coordination, quality assurance, and customer order fulfillment.

## PERSONAL INTEREST

With 20 years in industrial construction, I’ve witnessed recurring inefficiencies in materials management, from delayed procurement to inventory mismatches, costing companies millions. My interest is to empower organizations handling vast material flows, thousands of stakeholders, and critical timelines with a tool that provides early visibility into potential issues, enhances decision-making, and drives efficient, profitable outcomes through integrated data and analytics.

## SYSTEM DESCRIPTION

The MMS is a secure, cloud-based data aggregation system that integrates periodic feeds from disparate systems (e.g., Engineering, Procurement, Fabrication, Warehouse) without replacing their bespoke Systems of Record. It consumes data via API integrations where available or manual uploads for systems lacking API support. The MMS platform enables technologists to create connections, schedule ETL transformations, and store datasets for analytics. Key features include tracking materials from dock arrival to customer delivery, managing demand based on Engineering and Fabrication inputs, and supporting processes like inspection, maintenance, and inventory. MMS leverages Django REST Framework with Django ORM, SQLite (`mms.db`), and Celery with Redis in Docker for asynchronous tasks (e.g., demand reports, notifications). Standard reports and dashboards provide visibility into material status, demand alignment, and delivery progress, with predictive analytics for course corrections, ensuring seamless coordination across personas (Engineer, Procurement, Fabrication, etc.).
