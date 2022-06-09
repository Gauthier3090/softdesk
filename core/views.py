from rest_framework.viewsets import ReadOnlyModelViewSet
from core.models import User
from core.serializers import UserSerializer


class UserViewSet(ReadOnlyModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()
