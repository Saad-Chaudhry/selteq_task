from celery import shared_task
from django.utils.timezone import now
from core.models import Task


@shared_task
def print_user1_tasks():
    tasks = Task.objects.filter(user_id=1)
    print(f"--- Tasks for User ID 1 at {now()} ---")
    for task in tasks:
        print(f"Title: {task.title}, Duration: {task.duration}, Created: {task.created_at}")
