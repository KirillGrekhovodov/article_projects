from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from webapp.models import BaseModel


class Project(BaseModel):
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name="Название")
    users = models.ManyToManyField(
        get_user_model(),
        related_name="projects",
        blank=True
    )

    class Meta:
        db_table = "projects"
        permissions = [("add_users_in_project", "добвалять пользователей в проект")]
