from celery import shared_task
import time

@shared_task
def test_background_task():
    time.sleep(5)
    return "Task Completed"