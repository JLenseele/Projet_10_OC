from django.shortcuts import render
from rest_framework import request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Project
from .serializers import ProjectSerializer, ProjectDetailSerializer


class ProjectAPIView(ModelViewSet):

    serializer_class = ProjectSerializer
    detail_serializer_class = ProjectDetailSerializer

    def get_queryset(self):
        user = self.request.user
        print(user)
        return Project.objects.filter(author=user.id)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()


