from rest_framework.generics import CreateAPIView
from core.models import User
from core.serializers import UserSerializer
from rest_framework.permissions import AllowAny


class UserViewSet(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return User.objects.all()
