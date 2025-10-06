from celery import shared_task
import time

@shared_task
def notify_procurement_task(message):
    time.sleep(1)  # Simulate processing
    print(f"Procurement Notification: {message}")

@shared_task
def notify_engineer_task(message):
    time.sleep(1)  # Simulate processing
    print(f"Engineer Notification: {message}")

@shared_task
def notify_fabrication_task(message):
    time.sleep(1)  # Simulate processing
    print(f"Fabrication Notification: {message}")

@shared_task
def notify_warehouse_task(message):
    time.sleep(1)  # Simulate processing
    print(f"Warehouse Notification: {message}")

@shared_task
def notify_shipping_task(message):
    time.sleep(1)  # Simulate processing
    print(f"Shipping Notification: {message}")

@shared_task
def generate_demand_report_task(report_id, start_date, end_date):
    time.sleep(2)  # Simulate report generation
    print(f"Generated report {report_id} for dates {start_date} to {end_date}")

@shared_task
def send_notification_task(recipient_id, message):
    time.sleep(1)  # Simulate sending notification
    print(f"Notification sent to {recipient_id}: {message}")