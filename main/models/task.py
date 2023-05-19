from django.db import models
from .user import User
from .tag import Tag
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    header = models.CharField(max_length=50)
    body = models.CharField(max_length=1000)
    created_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)
    deadline_date = models.DateField()

    class States(models.TextChoices):
        NEWTASK = "new_task", _("New task")
        INDEV = "in_development", _("In development")
        INQA = "in_qa", _("In QA")
        INCR = "in_code_review", _("In code review")
        READY = "ready_for_release", _("Ready for release")
        RELEASED = "released", _("Released")
        ARCHIVED = "archived", _("Archived")

    state = models.CharField(
        max_length=17, choices=States.choices, default=States.NEWTASK
    )
    priority = models.BooleanField(default=False)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="author"
    )
    executor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="executor"
    )
    tags = models.ManyToManyField(Tag)
