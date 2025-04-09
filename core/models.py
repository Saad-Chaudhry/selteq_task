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
