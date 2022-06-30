from project.models import Project, Contributor, Issue, Comment
from rest_framework.serializers import ModelSerializer


class ProjectSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ('author', 'id')


class ContributorSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = '__all__'
        read_only__fields = ('project', 'role', 'id')


class IssueSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = '__all__'
        read_only__fields = ('project', 'author', 'created_time', 'id')


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only__fields = ('author', 'issue', 'created_time', 'id')
