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

    def test_create(self) -> None:
        tag = self.create(self.tag_attributes)
        expected_response = self.expected_details(tag, self.tag_attributes)
        assert tag == expected_response

    def test_list(self) -> None:
        tag_created = self.create(self.tag_attributes)
        tags_list = self.list()
        assert tags_list == [tag_created]

    def test_retrieve(self) -> None:
        tag_created = self.create(self.tag_attributes)
        tag_retrieved = self.retrieve(tag_created["id"])
        assert tag_retrieved == tag_created

    def test_update(self) -> None:
        tag_created = self.create(self.tag_attributes)
        new_tag_attributes = self.tag_attributes.copy()
        new_tag_attributes["title"] = "new_test_tag"
        tag_updated = self.update(tag_created["id"], new_tag_attributes)
        expected_response = self.expected_details(tag_created, new_tag_attributes)
        assert tag_updated == expected_response

    def test_delete_not_staff(self) -> None:
        tag = self.create(self.tag_attributes)
        response = self.delete(tag["id"])
        assert response

    def test_delete_staff(self) -> None:
        self.user.is_staff = True
        self.user.save()
        tag = self.create(self.tag_attributes)
        response = self.delete(tag["id"])
        assert response == None
        self.user.is_staff = False
        self.user.save()
