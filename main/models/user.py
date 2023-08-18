from django.contrib.auth.models import AbstractUser
from django.db import models
from main.services.storage_backends import public_storage


class User(AbstractUser):
    class Roles(models.TextChoices):
        DEVELOPER = "developer"
        MANAGER = "manager"
        ADMIN = "admin"

    role = models.CharField(
        max_length=255, default=Roles.DEVELOPER, choices=Roles.choices
    )
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    avatar_picture = models.ImageField(null=True, storage=public_storage, blank=True)

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name}) [{self.role}]"

    def attributes(self, with_avatar: bool = False):
        attr = {
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "role": self.role,
            "date_of_birth": self.date_of_birth,
            "phone": self.phone,
        }
        if with_avatar:
            attr["avatar_picture"] = self.avatar_picture
            return {key: value for key, value in attr.items() if value is not None}
        return attr
