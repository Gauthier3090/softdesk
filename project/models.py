from django.conf import settings
from django.db import models


TYPES = [
    ('BACKEND', 'BACKEND'),
    ('FRONTEND', 'FRONTEND'),
    ('IOS', 'IOS'),
    ('ANDROID', 'ANDROID')
]

ROLES = [
    ('AUTHOR', 'AUTHOR'),
    ('CONTRIBUTOR', 'CONTRIBUTOR')
]

TAGS = [
    ('BUG', 'BUG'),
    ('TASK', 'TASK'),
    ('UPGRADE', 'UPGRADE')
]

PRIORITIES = [
    ('LOW', 'LOW'),
    ('MEDIUM', 'MEDIUM'),
    ('HIGH', 'HIGH')
]

STATUES = [
    ('TODO', 'TODO'),
    ('IN PROGRESS', 'IN PROGRESS'),
    ('DONE', 'DONE')
]


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=5000)
    type = models.CharField(choices=TYPES, max_length=8)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author')


class Contributor(models.Model):
    user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project_id = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=11, choices=ROLES, default='CONTRIBUTOR')

    class Meta:
        unique_together = ('user_id', 'project_id')


class Issue(models.Model):
    title = models.CharField(max_length=150)
    desc = models.CharField(max_length=5000)
    tag = models.CharField(max_length=20)
    priority = models.CharField(choices=PRIORITIES, max_length=6, default="LOW")
    status = models.CharField(choices=STATUES, max_length=11, default="TODO")
    project_id = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="issue_id")
    assignee_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assignee")
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    description = models.CharField(max_length=5000)
    created_time = models.DateTimeField(auto_now_add=True)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue_id = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
