from http import HTTPStatus
from typing import List, Union

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from main.models import User


class TestViewSetBase(APITestCase):
    user: User = None
    client: APIClient = None
    basename: str

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user = cls.create_api_user()
        cls.client = APIClient()

    @classmethod
    def create_api_user(cls):
        return User.objects.create(**cls.user_attributes)

    @classmethod
    def detail_url(cls, key: int) -> str:
        return reverse(f"{cls.basename}-detail", args=[key])

    @classmethod
    def list_url(cls, args: List[Union[str, int]] = None) -> str:
        return reverse(f"{cls.basename}-list", args=args)

    def create(self, data: dict, args: List[Union[str, int]] = None) -> dict:
        self.client.force_login(self.user)
        response = self.client.post(self.list_url(args), data=data, format="json")
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data

    def list(self, data: dict = None, args: List[Union[str, int]] = None) -> dict:
        self.client.force_login(self.user)
        response = self.client.get(self.list_url(args), data=data)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def retrieve(self, key: int) -> dict:
        self.client.force_login(self.user)
        response = self.client.get(self.detail_url(key), data=None)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def update(self, key: int, data: dict) -> dict:
        self.client.force_login(self.user)
        response = self.client.put(self.detail_url(key), data=data)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def delete(self, key: int) -> dict:
        self.client.force_login(self.user)
        response = self.client.delete(self.detail_url(key), data=None)
        if self.user.is_staff:
            assert response.status_code == HTTPStatus.NO_CONTENT, response.content
        else:
            assert response.status_code == HTTPStatus.FORBIDDEN, response.content
        return response.data
