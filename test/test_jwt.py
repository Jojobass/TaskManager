from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from freezegun import freeze_time
from datetime import timedelta
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


class TestJWTAuth(APITestCase):
    token_url = reverse("token_obtain_pair")
    refresh_token_url = reverse("token_refresh")
    any_api_url = reverse("users-list")

    @staticmethod
    def create_user():
        return UserFactory.create()

    def token_request(self, username: str = None, password: str = "password"):
        client = self.client_class()
        if not username:
            username = self.create_user().username
        return client.post(
            self.token_url, data={"username": username, "password": password}
        )

    def refresh_token_request(self, refresh_token: str):
        client = self.client_class()
        return client.post(self.refresh_token_url, data={"refresh": refresh_token})

    def get_refresh_token(self):
        response = self.token_request()
        return response.json()["refresh"]

    def test_successful_auth(self):
        response = self.token_request()
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["refresh"]
        assert response.json()["access"]

    def test_unsuccessful_auth(self):
        response = self.token_request(username="incorrect_username")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_refresh_token(self):
        refresh_token = self.get_refresh_token()
        response = self.refresh_token_request(refresh_token)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["access"]

    def test_token_auth(self) -> None:
        client = self.client_class()
        response = client.get(self.any_api_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = self.token_request()
        token = response.json()["access"]
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = client.get(self.any_api_url)
        assert response.status_code == status.HTTP_200_OK

    def test_refresh_lives_lower_than_one_day(self) -> None:
        with freeze_time() as frozen_time:
            refresh_token = self.get_refresh_token()
            frozen_time.tick(timedelta(hours=23, minutes=59))
            response = self.refresh_token_request(refresh_token)
            assert response.status_code == status.HTTP_200_OK
            assert response.json()["access"]

    def test_refresh_dies_after_one_day(self) -> None:
        with freeze_time() as frozen_time:
            refresh_token = self.get_refresh_token()
            frozen_time.tick(timedelta(days=1))
            response = self.refresh_token_request(refresh_token)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
