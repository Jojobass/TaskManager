from unittest.mock import patch, MagicMock

from django.core import mail
from django.template.loader import render_to_string

from main.models import Task
from datetime import date
from main.services.mail import send_assign_notification
from base import TestViewSetBase


class TestSendEmail(TestViewSetBase):
    basename = "tasks"
    user_attributes = {
        "username": "johnsmith",
        "first_name": "John",
        "last_name": "Smith",
        "email": "john@test.com",
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

    @patch.object(mail, "send_mail")
    def test_send_assign_notification(self, fake_sender: MagicMock) -> None:
        assignee = self.user
        task = Task(**self.task_attributes, assignee=assignee)
        task.save()

        send_assign_notification(task.id)

        fake_sender.assert_called_once_with(
            subject="You've been assigned a task.",
            message="",
            from_email=None,
            recipient_list=[assignee.email],
            html_message=render_to_string(
                "emails/notification.html",
                context={"task": Task.objects.get(pk=task.id)},
            ),
        )
