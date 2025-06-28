from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

    def validate(self, data):
        if not data.get("title"):
            raise serializers.ValidationError("Title is required.")
        return data

    def create(self, validated_data):
        """
        Create a new task instance.
        """
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update an existing task instance.
        """
        return super().update(instance, validated_data)
