from base import TestViewSetBase, UserFactory
from http import HTTPStatus
from django.core.files.uploadedfile import SimpleUploadedFile


class TestUserViewSet(TestViewSetBase):
    basename = "users"
    user_attributes = {
        "username": "johnsmith",
        "first_name": "John",
        "last_name": "Smith",
        "email": "john@test.com",
        "role": "developer",
        "date_of_birth": "2001-01-01",
        "phone": "1111111111",
        "avatar_picture": None,
    }

    def expected_details(self, entity: dict, attributes: dict) -> dict:
        return {
            **attributes,
            "id": entity["id"],
            "avatar_picture": entity["avatar_picture"],
        }

    def test_create(self) -> None:
        user_attributes = UserFactory.build().attributes()
        user = self.create(user_attributes)
        expected_response = self.expected_details(user, user_attributes)
        assert user == expected_response

    def test_list(self) -> None:
        user_attributes = UserFactory.build().attributes()
        user_created = self.create(user_attributes)
        user_default = self.user_attributes.copy()
        user_default["id"] = self.user.id
        users_list = self.list()
        assert list(map(dict, users_list)) == [user_default, user_created]

    def test_retrieve(self) -> None:
        user_attributes = UserFactory.build().attributes()
        user_created = self.create(user_attributes)
        user_retrieved = self.retrieve(user_created["id"])
        assert user_retrieved == user_created

    def test_update(self) -> None:
        user_attributes = UserFactory.build().attributes()
        user_created = self.create(user_attributes)
        new_user_attributes = user_attributes.copy()
        new_user_attributes["first_name"] = "User"
        user_updated = self.update(user_created["id"], new_user_attributes)

        expected_response = self.expected_details(user_created, new_user_attributes)
        expected_response["avatar_picture"] = user_updated["avatar_picture"]
        assert user_updated == expected_response

    def test_delete_not_staff(self) -> None:
        user_attributes = UserFactory.build().attributes()
        user = self.create(user_attributes)
        response = self.delete(user["id"])
        assert response

    def test_delete_staff(self) -> None:
        self.user.is_staff = True
        self.user.save()
        user_attributes = UserFactory.build().attributes()
        user = self.create(user_attributes)
        response = self.delete(user["id"])
        assert response is None

    def test_large_avatar(self) -> None:
        user_attributes = UserFactory.build(
            avatar_picture=SimpleUploadedFile("large.jpg", b"x" * 2 * 1024 * 1024)
        ).attributes(True)
        response = self.request_create(user_attributes)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {"avatar_picture": ["Maximum size 1048576 exceeded."]}

    def test_avatar_bad_extension(self) -> None:
        user_attributes = UserFactory.build().attributes(True)
        user_attributes["avatar_picture"].name = "bad_extension.pdf"
        response = self.request_create(user_attributes)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {
            "avatar_picture": [
                "File extension “pdf” is not allowed. Allowed extensions are: jpeg, jpg, png."
            ]
        }
