from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
import django_filters
from .models import User, Task, Tag
from .serializers import UserSerializer, TagSerializer, TaskSerializer


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = {
            "username": ["icontains"],
            "first_name": ["icontains"],
            "last_name": ["icontains"],
        }


class TagFilter(django_filters.FilterSet):
    class Meta:
        model = Tag
        fields = {
            "title": ["icontains"],
        }


class TaskFilter(django_filters.FilterSet):
    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(), conjoined=True, lookup_expr="exact"
    )

    class Meta:
        model = Task
        fields = {
            "title": ["icontains"],
            "state": ["icontains"],
            "assignee__username": ["icontains"],
            "assignee__first_name": ["icontains"],
            "assignee__last_name": ["icontains"],
            "author__username": ["icontains"],
            "author__first_name": ["icontains"],
            "author__last_name": ["icontains"],
        }


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer
    filterset_class = UserFilter


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.order_by("id")
    serializer_class = TagSerializer
    filterset_class = TagFilter


class TaskViewSet(viewsets.ModelViewSet):
    queryset = (
        Task.objects.select_related("author", "assignee")
        .prefetch_related("tags")
        .order_by("id")
    )
    serializer_class = TaskSerializer
    filterset_class = TaskFilter
