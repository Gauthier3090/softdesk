from project.models import Project, Contributor
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
