from djoser.views import UserViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User
from .serializers import CustomUserSerializer


class CustomUserViewSet(UserViewSet):
    """View Set for all user endpoints."""
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'id'

    def perform_create(self, serializer, *args, **kwargs):
        serializer.save(*args, **kwargs)

    @action(methods=['GET'], detail=False,
            permission_classes=(permissions.IsAuthenticated,))
    def me(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
