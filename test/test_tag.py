from base import TestViewSetBase


class TestTagViewSet(TestViewSetBase):
    basename = "tags"
    user_attributes = {
        "username": "johnsmith",
        "first_name": "John",
        "last_name": "Smith",
        "email": "john@test.com",
        "role": "developer",
    }
    tag_data = {"title": "test_tag"}

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    @staticmethod
    def expected_list(entities: list[dict], attributes: dict):
        return [{**attributes, "id": entities[0]["id"]}]

    def test_create(self):
        tag = self.create(self.tag_data)
        expected_response = self.expected_details(tag, self.tag_data)
        assert tag == expected_response

    def test_list(self):
        self.create(self.tag_data)
        tags = self.list(self.tag_data)
        expected_response = self.expected_list(tags, self.tag_data)
        assert list(map(dict, tags)) == expected_response

    def test_retrieve(self):
        tag = self.create(self.tag_data)
        tag = self.retrieve(tag["id"])
        expected_response = self.expected_details(tag, self.tag_data)
        assert tag == expected_response

    def test_update(self):
        tag = self.create(self.tag_data)
        new_tag_data = self.tag_data.copy()
        new_tag_data["title"] = "new_test_tag"
        tag = self.update(tag["id"], new_tag_data)
        expected_response = self.expected_details(tag, new_tag_data)
        assert tag == expected_response

    def test_delete(self):
        tag = self.create(self.tag_data)
        response = self.delete(tag["id"])
        assert response


class TestTagDeleteByStaff(TestViewSetBase):
    basename = "tags"
    user_attributes = {
        "username": "johnsmith",
        "first_name": "John",
        "last_name": "Smith",
        "email": "john@test.com",
        "role": "developer",
        "is_staff": True,
    }
    tag_data = {"title": "test_tag"}

    def test_delete(self):
        tag = self.create(self.tag_data)
        response = self.delete(tag["id"])
        assert response == None
