from rest_framework.serializers import ModelSerializer
from issuetracking.models import Project
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class ProjectSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'author']


class ProjectDetailSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'type', 'status', 'author']