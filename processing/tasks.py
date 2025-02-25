from celery import shared_task
import time

@shared_task
def long_running_task(unique_id):
    """
    Simulate a long-running background task.
    """
    print(f"Starting background job with ID: {unique_id}")
    time.sleep(10)  # Simulating a long task (10 seconds)
    print(f"Background job with ID: {unique_id} is complete.")
