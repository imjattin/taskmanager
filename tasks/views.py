from django_filters import rest_framework as filters
from rest_framework import viewsets

from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ["completed"]
