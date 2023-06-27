from base import TestViewSetBase

from main.models import User
from datetime import date


class TestTaskViewSet(TestViewSetBase):
    basename = "tasks"
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
    task_attributes = {
        "title": "test_task",
        "description": "test task desc",
        "created_date": str(date.today()),
        "modified_date": str(date.today()),
        "state": "new_task",
        "priority": False,
    }

    @staticmethod
    def expected_details(entity: dict, attributes: dict) -> dict:
        return {
            **attributes,
            "id": entity["id"],
            "author": None,
            "assignee": None,
            "deadline_date": None,
            "tags": [],
        }

    def test_create(self) -> None:
        task = self.create(self.task_attributes)
        expected_response = self.expected_details(task, self.task_attributes)
        assert task == expected_response

    def test_list(self) -> None:
        task_created = self.create(self.task_attributes)
        tasks_list = self.list()
        assert tasks_list == [task_created]

    def test_retrieve(self) -> None:
        task_created = self.create(self.task_attributes)
        task_retrieved = self.retrieve(task_created["id"])
        assert task_retrieved == task_created

    def test_update(self) -> None:
        task_created = self.create(self.task_attributes)
        new_task_attributes = self.task_attributes.copy()
        new_task_attributes["title"] = "new_test_task"
        task_updated = self.update(task_created["id"], new_task_attributes)
        expected_response = self.expected_details(task_created, new_task_attributes)
        assert task_updated == expected_response

    def test_delete_not_staff(self) -> None:
        task = self.create(self.task_attributes)
        response = self.delete(task["id"])
        assert response

    def test_delete_staff(self) -> None:
        self.user.is_staff = True
        self.user.save()
        task = self.create(self.task_attributes)
        response = self.delete(task["id"])
        assert response == None
