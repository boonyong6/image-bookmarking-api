from django.contrib.auth import get_user_model
from oauth2_provider.contrib.rest_framework.permissions import TokenHasReadWriteScope
from rest_framework import mixins, permissions, viewsets

from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,  # TODO: Should be `AllowAny`.
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer
