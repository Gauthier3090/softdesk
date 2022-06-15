from project.models import Project
from rest_framework.serializers import ModelSerializer


class ProjectSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ('author', 'id')
