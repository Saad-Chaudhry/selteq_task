from rest_framework import serializers
from ...models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'duration', 'created_at', 'updated_at']

    def create(self, validated_data):
        title = validated_data.get('title')
        duration = validated_data.get('duration')

        if not title:
            raise serializers.ValidationError({"title": "This field is required."})
        if duration is None:
            raise serializers.ValidationError({"duration": "This field is required."})

        user = self.context['request'].user

        return Task.objects.create(user=user, **validated_data)
