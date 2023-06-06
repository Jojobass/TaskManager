from http import HTTPStatus
from typing import List, Union

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from factory.django import DjangoModelFactory
from factory import PostGenerationMethodCall, LazyAttribute
from faker import Faker

from main.models import User

fake = Faker()


def generate_username(*args):
    """returns a random username"""
    return fake.profile(fields=["username"])["username"]


class UserFactory(DjangoModelFactory):
    username = LazyAttribute(generate_username)
    password = PostGenerationMethodCall("set_password", "password")
    is_staff = False

    class Meta:
        model = User


class TestViewSetBase(APITestCase):
    user: User = None
    client: APIClient = None
    basename: str
    token_url = reverse("token_obtain_pair")
    refresh_token_url = reverse("token_refresh")

    @classmethod
    def token_request(cls, password: str = "password"):
        return cls.client.post(
            cls.token_url, data={"username": cls.user.username, "password": password}
        )

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user = cls.create_api_user()
        cls.client = APIClient()

    def setUp(self):
        response = self.token_request()
        token = response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    @classmethod
    def create_api_user(cls):
        return UserFactory.create(**cls.user_attributes)

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
