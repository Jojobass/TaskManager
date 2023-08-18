from http import HTTPStatus
from typing import List, Union

from django.urls import reverse
from django.http import HttpResponse
from rest_framework.test import APIClient, APITestCase
from factory.django import DjangoModelFactory
from factory import PostGenerationMethodCall, LazyAttribute
from faker import Faker
from django.core.files.uploadedfile import SimpleUploadedFile
from faker.providers import BaseProvider

from main.models import User

fake = Faker()


class ImageFileProvider(BaseProvider):
    def image_file(self, fmt: str = "jpeg") -> SimpleUploadedFile:
        return SimpleUploadedFile(
            self.generator.file_name(extension=fmt),
            self.generator.image(image_format=fmt),
        )


fake.add_provider(ImageFileProvider)


def generate_username(*args):
    return fake.profile(fields=["username"])["username"]


class UserFactory(DjangoModelFactory):
    username = LazyAttribute(generate_username)
    password = PostGenerationMethodCall("set_password", "password")
    is_staff = False
    avatar_picture = fake.image_file(fmt="jpeg")

    class Meta:
        model = User


class TestViewSetBase(APITestCase):
    user: User = None
    client: APIClient = None
    basename: str
    token_url = reverse("token_obtain_pair")
    refresh_token_url = reverse("token_refresh")

    @classmethod
    def token_request(cls, password: str = "password") -> HttpResponse:
        return cls.client.post(
            cls.token_url, data={"username": cls.user.username, "password": password}
        )

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user = cls.create_api_user()
        cls.client = APIClient()
        cls.client.force_login(cls.user)

    def setUp(self) -> None:
        response = self.token_request()
        token = response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    @classmethod
    def create_api_user(cls) -> User:
        return UserFactory.create(**cls.user_attributes)

    @classmethod
    def detail_url(cls, key: int) -> str:
        return reverse(f"{cls.basename}-detail", args=[key])

    @classmethod
    def list_url(cls, args: List[Union[str, int]] = None) -> str:
        return reverse(f"{cls.basename}-list", args=args)

    @staticmethod
    def expected_details(entity: dict, attributes: dict) -> dict:
        return {**attributes, "id": entity["id"]}

    def create(
        self, data: dict, args: List[Union[str, int]] = None, fmt: str = "json"
    ) -> dict:
        response = self.client.post(self.list_url(args), data=data, format=fmt)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data

    def request_create(self, data: dict, args: List[Union[str, int]] = None):
        return self.client.post(self.list_url(args), data=data, format="multipart")

    def list(self, data: dict = None, args: List[Union[str, int]] = None) -> dict:
        response = self.client.get(self.list_url(args), data=data)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def retrieve(self, key: int) -> dict:
        response = self.client.get(self.detail_url(key), data=None)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def update(self, key: int, data: dict) -> dict:
        response = self.client.put(self.detail_url(key), data=data, format="json")
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def delete(self, key: int) -> dict:
        response = self.client.delete(self.detail_url(key), data=None)
        if self.user.is_staff:
            assert response.status_code == HTTPStatus.NO_CONTENT, response.content
        else:
            assert response.status_code == HTTPStatus.FORBIDDEN, response.content
        return response.data
