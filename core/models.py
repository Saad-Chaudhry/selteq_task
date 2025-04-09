from django.contrib.auth.models import AbstractUser
from django.db import models

from core.managers import CustomUserManager


class User(AbstractUser):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['-id']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    duration = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tasks_task'

    def __str__(self):
        return self.title
