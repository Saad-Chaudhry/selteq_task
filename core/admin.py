from django.contrib import admin
from .models import User, Task


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration', 'created_at', 'updated_at')
    search_fields = ('title',)
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)
