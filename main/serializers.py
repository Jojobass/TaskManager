from rest_framework import serializers
from .models import User, Tag, Task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
        )  # 'date_of_birth', 'phone' (are they necessary?)
        read_only_fields = ["id"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("title",)


class TaskSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    assignee = UserSerializer(required=False)
    tags = TagSerializer(required=False, many=True)

    class Meta:
        model = Task
        fields = (
            "title",
            "description",
            "created_date",
            "modified_date",
            "deadline_date",
            "state",
            "priority",
            "author",
            "assignee",
            "tags",
        )
