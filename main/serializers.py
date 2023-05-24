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
        model = Tag
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

    def create(self, validated_data):
        author_data = validated_data.pop("author")
        assignee_data = validated_data.pop("assignee", None)
        tags_data = validated_data.pop("tags", [])
        author, created = User.objects.get_or_create(**author_data)
        task = Task.objects.create(author=author, **validated_data)
        if assignee_data:
            assignee, created = User.objects.get_or_create(**assignee_data)
            task.assignee = assignee
        task.tags.set(self.get_or_create_packages(tags_data))
        return task

    def update(self, instance, validated_data):
        author = instance.author
        assignee = instance.assignee
        author_data = validated_data.pop("author")
        assignee_data = validated_data.pop("assignee", None)
        tags_data = validated_data.pop("tags", [])

        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.created_date = validated_data.get(
            "created_date", instance.created_date
        )
        instance.modified_date = validated_data.get(
            "modified_date", instance.modified_date
        )
        instance.deadline_date = validated_data.get(
            "deadline_date", instance.deadline_date
        )
        instance.state = validated_data.get("state", instance.state)
        instance.priority = validated_data.get("priority", instance.priority)
        instance.tags.set(self.get_or_create_tags(tags_data))
        instance.save()

        author.username = author_data.get("username", author.username)
        author.first_name = author_data.get("first_name", author.first_name)
        author.last_name = author_data.get("last_name", author.last_name)
        author.email = author_data.get("email", author.email)
        author.role = author_data.get("role", author.role)
        author.save()

        assignee.username = assignee_data.get("username", assignee.username)
        assignee.first_name = assignee_data.get("first_name", assignee.first_name)
        assignee.last_name = assignee_data.get("last_name", assignee.last_name)
        assignee.email = assignee_data.get("email", assignee.email)
        assignee.role = assignee_data.get("role", assignee.role)
        assignee.save()

        return instance

    def get_or_create_tags(self, tags_data):
        tag_ids = []
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(**tag_data)
            tag_ids.append(tag.id)
        return tag_ids
