from base import TestViewSetBase

from main.models import User
from datetime import date


class TestUserViewSet(TestViewSetBase):
    basename = "tasks"
    user_attributes = {
        "username": "johnsmith",
        "first_name": "John",
        "last_name": "Smith",
        "email": "john@test.com",
        "role": "developer",
    }
    user_data = {
        "username": "user_for_testing",
        "first_name": "user",
        "last_name": "for testing",
        "email": "user@test.com",
        "role": "developer",
    }
    task_data = {"title": "test_task", "description": "test task desc"}

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    @staticmethod
    def expected_list(entities: list[dict], attributes: dict):
        return [{**attributes, "id": entities[0]["id"]}]

    def test_create(self):
        print(self.task_data)
        task = self.create(self.task_data)
        expected_response = self.expected_details(task, self.task_data)
        assert {
            key: task[key] for key in ["id", "title", "description"]
        } == expected_response

    def test_list(self):
        task = self.create(self.task_data)
        tasks = self.list(self.task_data)
        expected_response = self.expected_list(tasks, self.task_data)
        assert {
            key: list(map(dict, tasks))[0][key]
            for key in ["id", "title", "description"]
        } == expected_response[0]

    def test_retrieve(self):
        task = self.create(self.task_data)
        task = self.retrieve(task["id"])
        expected_response = self.expected_details(task, self.task_data)
        assert {
            key: task[key] for key in ["id", "title", "description"]
        } == expected_response

    def test_update(self):
        task = self.create(self.task_data)
        new_task_data = self.task_data.copy()
        new_task_data["title"] = "new_test_task"
        task = self.update(task["id"], new_task_data)
        expected_response = self.expected_details(task, new_task_data)
        assert {
            key: task[key] for key in ["id", "title", "description"]
        } == expected_response

    def test_delete(self):
        task = self.create(self.task_data)
        response = self.delete(task["id"])
        assert response


class TestTagDeleteByStaff(TestViewSetBase):
    basename = "tasks"
    user_attributes = {
        "username": "johnsmith",
        "first_name": "John",
        "last_name": "Smith",
        "email": "john@test.com",
        "role": "developer",
        "is_staff": True,
    }
    user_data = {
        "username": "user_for_testing",
        "first_name": "user",
        "last_name": "for testing",
        "email": "user@test.com",
        "role": "developer",
    }
    task_data = {"title": "test_task", "description": "test task desc"}

    def test_delete(self):
        task = self.create(self.task_data)
        response = self.delete(task["id"])
        assert response == None
