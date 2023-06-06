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
    tag_attributes = {"title": "test_tag"}

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def test_create(self):
        tag = self.create(self.tag_attributes)
        expected_response = self.expected_details(tag, self.tag_attributes)
        assert tag == expected_response

    def test_list(self):
        self.create(self.tag_attributes)
        tags = self.list(self.tag_attributes)
        expected_response = self.expected_details(tags[0], self.tag_attributes)
        assert tags == [expected_response]

    def test_retrieve(self):
        tag = self.create(self.tag_attributes)
        tag = self.retrieve(tag["id"])
        expected_response = self.expected_details(tag, self.tag_attributes)
        assert tag == expected_response

    def test_update(self):
        tag = self.create(self.tag_attributes)
        new_tag_data = self.tag_attributes.copy()
        new_tag_data["title"] = "new_test_tag"
        tag = self.update(tag["id"], new_tag_data)
        expected_response = self.expected_details(tag, new_tag_data)
        assert tag == expected_response

    def test_delete_not_staff(self):
        tag = self.create(self.tag_attributes)
        response = self.delete(tag["id"])
        assert response

    def test_delete_staff(self):
        self.user.is_staff = True
        self.user.save()
        print(self.user.is_staff)
        tag = self.create(self.tag_attributes)
        response = self.delete(tag["id"])
        assert response == None
