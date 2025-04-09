from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.db import connection
from ...models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by('-created_at')[:4]

    def perform_create(self, serializer):
        serializer.save()

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        user_id = request.user.id
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, title, duration, created_at, updated_at FROM tasks_task WHERE id=%s AND user_id=%s",
                [pk, user_id]
            )
            row = cursor.fetchone()
        if not row:
            return Response({'detail': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'id': row[0],
            'title': row[1],
            'duration': row[2],
            'created_at': row[3],
            'updated_at': row[4],
        })

    def update(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        title = request.data.get('title')
        user_id = request.user.id

        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE tasks_task SET title=%s WHERE id=%s AND user_id=%s",
                [title, pk, user_id]
            )
            row = cursor.rowcount
        if not row:
            return Response({'detail': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'detail': 'Title updated successfully'}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            task = Task.objects.get(pk=pk, user=request.user)
            task.delete()
            return Response({'detail': 'Task deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            return Response({'detail': 'Task not found or unauthorized'}, status=status.HTTP_404_NOT_FOUND)
