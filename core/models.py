from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=25, default="")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)


class Project(models.Model):
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=5000)
    type = models.CharField(max_length=15)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Contributor(models.Model):
    user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project_id = models.ForeignKey(to=Project, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user_id', 'project_id')


class Issue(models.Model):
    title = models.CharField(max_length=150)
    desc = models.CharField(max_length=5000)
    tag = models.CharField(max_length=20)
    priority = models.CharField(max_length=10)
    status = models.CharField(max_length=20)
    project_id = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="issue_id")
    assignee_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assignee")
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    description = models.CharField(max_length=5000)
    created_time = models.DateTimeField(auto_now_add=True)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue_id = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
