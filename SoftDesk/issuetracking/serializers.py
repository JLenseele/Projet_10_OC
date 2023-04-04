from rest_framework.serializers import ModelSerializer
from issuetracking.models import Project, Contributor, Issue, Comments
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class ProjectSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'author']


class ContributorSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'role', 'permission', 'project']


class ContributorProjectSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['user', 'permission']


class ProjectDetailSerializer(ModelSerializer):

    contributors = ContributorSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'type', 'status', 'author', 'contributors']


class IssueSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title', 'priority', 'project_id', 'author', 'assign']


class IssueProjectSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title', 'desc', 'tag', 'priority', 'status', 'assign']


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comments
        fields = ['id', 'desc', 'created_time', 'author', 'issue']


class CommentIssueSerializer(ModelSerializer):

    class Meta:
        model = Comments
        fields = ['desc']