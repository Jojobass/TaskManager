from django.test import RequestFactory
from rest_framework.test import APITestCase
from rest_framework import permissions

from main.models import User
from main.views import IsStaffDeletePolicy


class TestDeletePermissionsViewSet(APITestCase):
    permission_check: permissions.BasePermission
    factory: RequestFactory

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.permission_check = IsStaffDeletePolicy()
        cls.factory = RequestFactory()

    def create_user(self, is_staff_):
        user = User(username="test_user", password="pass", is_staff=is_staff_)
        user.username = "staff_user" if is_staff_ else "non_staff_user"
        user.save()

        return user

    def delete_as(self, user):
        request = self.factory.delete("/api/")
        request.user = user
        return self.permission_check.has_object_permission(request, None, None)

    def test_delete_staff(self):
        user = self.create_user(True)
        self.assertTrue(self.delete_as(user))

    def test_delete_not_staff(self):
        user = self.create_user(False)
        self.assertFalse(self.delete_as(user))
