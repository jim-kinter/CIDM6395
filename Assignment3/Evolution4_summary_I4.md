# Evolution 4 Summary: API Implementation

## Overview

Evolution 4 focused on implementing the Django REST Framework (DRF) API for the Materials Management System (MMS), activating the endpoints defined in `Evolution_2/api_design.md`. The goal was to enable full CRUD (Create, Read, Update, Delete) operations and beyond-CRUD functionality (e.g., material demand reports, notifications) for all MMS entities, integrating asynchronous task processing with Celery and Redis. This evolution brought the system to a fully functional state, allowing personas (Engineer, Procurement, Fabrication, Warehouse, Shipping) to interact with MMS via API requests.

## Objectives

- **Implement DRF API**: Create DRF viewsets to handle CRUD and beyond-CRUD operations for entities (`Material`, `Requirement`, `Widget`, etc.).
- **Define URL Patterns**: Configure URL routing for API endpoints.
- **Integrate Celery and Redis**: Implement asynchronous tasks (e.g., notifications, report generation) using Celery with Redis as the message broker.
- **Test API Functionality**: Validate endpoints and task execution using `curl` requests.

## Deliverables

- **Updated Files**:
  - `mms/apps/views.py`: Added DRF viewsets (`MaterialViewSet`, `RequirementViewSet`, etc.) to handle API endpoints, including custom actions (e.g., `arrival`, `feedback`, `report`).
  - `mms/apps/tasks.py`: Created Celery tasks (`notify_procurement_task`, `generate_demand_report_task`, etc.) for asynchronous operations.
  - `mms/urls.py` and `mms/apps/urls.py`: Configured URL routing for API endpoints (e.g., `/api/materials/`, `/api/requirements/`).
  - `mms/mms/settings.py`: Updated Celery configuration to use the `solo` pool (`CELERY_WORKER_POOL = 'solo'`) to resolve Windows-specific multiprocessing issues. This could be a problem if moved into a production environment but the root cause of this seems to be something with OneDrive so as long as the production environment wasn't on a OneDrive repository, the issue may be moot.

- **Testing**:
  - Successfully tested API endpoints using `curl`:
    - `POST /api/materials/arrival/`: Created a material with `status: "Received"`, triggering a Celery notification.
    - `POST /api/materials/report/`: Generated a demand report, triggering a Celery task.
  - Verified Celery task execution via worker logs (e.g., `Warehouse Notification: Inspection task assigned for material arrival.`).

## Challenges and Resolutions

- **Redis Installation**:
  - **Challenge**: The `redis-server` command failed because Redis was running in a Docker container, not on the host system.
  - **Resolution**: Verified the Docker container (`docker ps`), ensured port mapping (`0.0.0.0:6379->6379/tcp`), and confirmed connectivity (`docker exec -it redis-container redis-cli ping` returned `PONG`).

- **Celery PermissionError on Windows**:
  - **Challenge**: The Celery worker failed with `PermissionError: [WinError 5] Access is denied` due to `billiard`’s multiprocessing in a OneDrive directory.
  - **Resolution**: Configured Celery to use the `solo` pool (`CELERY_WORKER_POOL = 'solo'`) in `mms/mms/settings.py`, avoiding multiprocessing issues. This allowed the worker to run successfully.

- **Field Mismatch in API Request**:
  - **Challenge**: The `POST /api/materials/arrival/` endpoint returned `{"type":["This field is required."]}`, as the request used `material_type` but `MaterialSerializer` expected `type`.
  - **Resolution**: Updated `MaterialViewSet`’s `arrival` action to map `material_type` to `type` before serialization, ensuring compatibility with the serializer.

- **Terminal Management**:
  - **Challenge**: Running the Django server (`python manage.py runserver`) tied up the terminal, making it unclear how to run the Celery worker.
  - **Resolution**: Used two terminals—one for the Django server and one for the Celery worker—allowing simultaneous monitoring of both processes during development.

## Outcomes

- **API Functionality**: The DRF API is fully implemented, supporting all CRUD operations (e.g., `GET /api/materials/`, `POST /api/requirements/`) and beyond-CRUD actions (e.g., `POST /api/materials/report/`, `POST /api/notifications/notify/`).
- **Asynchronous Processing**: Celery tasks are executing correctly, handling notifications and report generation asynchronously with Redis as the message broker.
- **Stability on Windows**: Resolved Windows-specific issues (e.g., `PermissionError`) by configuring Celery’s concurrency model, ensuring a stable development environment.
- **Testing Success**: All API endpoints and Celery tasks passed tests, confirming the system’s functionality for all personas.

Evolution 4 successfully activated the MMS API, enabling seamless interaction with the system via HTTP requests and asynchronous task processing, paving the way for Evolution 5’s focus on documentation and testing.
