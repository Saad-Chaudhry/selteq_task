from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.api.v1.viewsets import TaskViewSet

router = DefaultRouter()
router.register('task', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
]
