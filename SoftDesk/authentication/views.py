from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import SelfAccount
from .models import User
from rest_framework.viewsets import ModelViewSet

from .serializers import UserSerializer, UserDetailSerializer


class CreateUserAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AccountUserAPIView(ModelViewSet):

    serializer_class = UserDetailSerializer
    permission_classes = [SelfAccount]

    def get_queryset(self):
        user = self.request.user
        queryset = User.objects.filter(id=user.id)
        return queryset
