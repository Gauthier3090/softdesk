from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.generics import get_object_or_404
from .models import Project


class ProjectPermissions(BasePermission):
    def has_permission(self, request, view):
        try:
            project = get_object_or_404(Project, id=view.kwargs['pk'])
            if request.method in SAFE_METHODS:
                return project in Project.objects.filter(contributor__user_id=request.user)
            return request.user == project.author_user_id
        except KeyError:
            return True


class ContributorPermissions(BasePermission):
    def has_permission(self, request, view):
        project = get_object_or_404(Project, id=view.kwargs['pk'])
        if request.method in SAFE_METHODS:
            return project in Project.objects.filter(contributor__user_id=request.user)
        return request.user == project.author_user_id