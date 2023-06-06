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
    def expected_details(entity: dict, attributes: dict):
        return {
            **attributes,
            "id": entity["id"],
            "author": None,
            "assignee": None,
            "deadline_date": None,
            "tags": [],
        }

    def test_create(self):
        print(self.task_attributes)
        task = self.create(self.task_attributes)
        expected_response = self.expected_details(task, self.task_attributes)
        assert task == expected_response

    def test_list(self):
        self.create(self.task_attributes)
        tasks = self.list(self.task_attributes)
        expected_response = self.expected_details(tasks[0], self.task_attributes)
        assert tasks == [expected_response]

    def test_retrieve(self):
        task = self.create(self.task_attributes)
        task = self.retrieve(task["id"])
        expected_response = self.expected_details(task, self.task_attributes)
        assert task == expected_response

    def test_update(self):
        task = self.create(self.task_attributes)
        new_task_data = self.task_attributes.copy()
        new_task_data["title"] = "new_test_task"
        task = self.update(task["id"], new_task_data)
        expected_response = self.expected_details(task, new_task_data)
        assert task == expected_response

    def test_delete_not_staff(self):
        task = self.create(self.task_attributes)
        response = self.delete(task["id"])
        assert response

    def test_delete_staff(self):
        self.user.is_staff = True
        self.user.save()
        task = self.create(self.task_attributes)
        response = self.delete(task["id"])
        assert response == None
