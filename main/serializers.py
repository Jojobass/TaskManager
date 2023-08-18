from rest_framework import serializers
from .models import User, Tag, Task
from django.core.files.base import File
from django.core.exceptions import ValidationError
from task_manager.settings import UPLOAD_MAX_SIZES
from django.core.validators import FileExtensionValidator


class FileMaxSizeValidator:
    def __init__(self, max_size: int) -> None:
        self.max_size = max_size

    def __call__(self, value: File) -> None:
        if value.size > self.max_size:
            raise ValidationError(f"Maximum size {self.max_size} exceeded.")


class UserSerializer(serializers.ModelSerializer):
    avatar_picture = serializers.FileField(
        required=False,
        allow_empty_file=True,
        validators=[
            FileMaxSizeValidator(UPLOAD_MAX_SIZES["avatar_picture"]),
            FileExtensionValidator(["jpeg", "jpg", "png"]),
        ],
    )

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "date_of_birth",
            "phone",
            "avatar_picture",
        )
        read_only_fields = ["id"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "id",
            "title",
        )
        read_only_fields = ["id"]


class TaskSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False)
    assignee = UserSerializer(required=False)
    tags = TagSerializer(required=False, many=True)

    class Meta:
        model = Task
        fields = (
            "id",
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
        read_only_fields = ["id"]
