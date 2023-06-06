from base import TestViewSetBase


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
    }

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    @staticmethod
    def expected_list(entities: list[dict], attributes: dict):
        return [{**attributes, "id": entities[0]["id"]}]

    def test_create(self):
        data = {
            "username": "user_for_testing",
            "first_name": "user",
            "last_name": "for testing",
            "email": "user@test.com",
            "role": "developer",
            "date_of_birth": "2000-01-01",
            "phone": "0000000000",
        }
        user = self.create(data)
        expected_response = self.expected_details(user, data)
        assert user == expected_response

    def test_list(self):
        users = self.list(self.user_attributes)
        expected_response = self.expected_list(users, self.user_attributes)
        assert list(map(dict, users)) == expected_response

    def test_retrieve(self):
        user = self.retrieve(self.user.id)
        expected_response = self.expected_details(user, self.user_attributes)
        assert user == expected_response

    def test_update(self):
        new_user_attributes = self.user_attributes.copy()
        new_user_attributes["first_name"] = "User"
        user = self.update(self.user.id, new_user_attributes)
        expected_response = self.expected_details(user, new_user_attributes)
        assert user == expected_response

    def test_delete(self):
        data = {
            "username": "user_for_testing",
            "first_name": "user",
            "last_name": "for testing",
            "email": "user@test.com",
            "role": "developer",
            "date_of_birth": "2000-01-01",
            "phone": "0000000000",
        }
        user = self.create(data)
        response = self.delete(user["id"])
        assert response


class TestUserDeleteByStaff(TestViewSetBase):
    basename = "users"
    user_attributes = {
        "username": "johnsmith",
        "first_name": "John",
        "last_name": "Smith",
        "email": "john@test.com",
        "role": "developer",
        "is_staff": True,
        "date_of_birth": "2001-01-01",
        "phone": "1111111111",
    }

    def test_delete(self):
        data = {
            "username": "user_for_testing",
            "first_name": "user",
            "last_name": "for testing",
            "email": "user@test.com",
            "role": "developer",
            "date_of_birth": "2000-01-01",
            "phone": "0000000000",
        }
        user = self.create(data)
        response = self.delete(user["id"])
        assert response == None
