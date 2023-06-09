from base import TestViewSetBase


class TestUserViewSet(TestViewSetBase):
    basename = "users"
    user_attributes = {
        "username": "johnsmith",
        "first_name": "John",
        "last_name": "Smith",
        "email": "john@test.com",
        "role": "developer",
    }
    user_attributes1 = {
        "username": "user_for_testing",
        "first_name": "user",
        "last_name": "for testing",
        "email": "user@test.com",
        "role": "developer",
    }

    def test_create(self) -> None:
        user = self.create(self.user_attributes1)
        expected_response = self.expected_details(user, self.user_attributes1)
        assert user == expected_response

    def test_list(self) -> None:
        user_created = self.create(self.user_attributes1)
        user_default = self.user_attributes.copy()
        user_default["id"] = self.user.id
        users_list = self.list()
        assert users_list == [user_default, user_created]

    def test_retrieve(self) -> None:
        user_created = self.create(self.user_attributes1)
        user_retrieved = self.retrieve(user_created["id"])
        assert user_retrieved == user_created

    def test_update(self) -> None:
        user_created = self.create(self.user_attributes1)
        new_user_attributes = self.user_attributes1.copy()
        new_user_attributes["first_name"] = "User"
        user_updated = self.update(user_created["id"], new_user_attributes)
        expected_response = self.expected_details(user_created, new_user_attributes)
        assert user_updated == expected_response

    def test_delete_not_staff(self) -> None:
        user = self.create(self.user_attributes1)
        response = self.delete(user["id"])
        assert response

    def test_delete_staff(self) -> None:
        self.user.is_staff = True
        self.user.save()
        user = self.create(self.user_attributes1)
        response = self.delete(user["id"])
        assert response == None
