from django.core.management.base import BaseCommand
from time import sleep

from core.models import Task


class Command(BaseCommand):
    help = 'Print all tasks one by one every 10 seconds'

    def handle(self, *args, **kwargs):
        while True:
            tasks = Task.objects.all()
            for task in tasks:
                self.stdout.write(f'{task.title}, {task.duration}, {task.created_at}')
                sleep(10)
            break
