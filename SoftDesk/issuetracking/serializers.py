from rest_framework.serializers import ModelSerializer
from .models import Project, Contributor, Issue, Comments


class ProjectSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'author', 'contributors', 'issues']


class ContributorSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['user', 'id', 'role', 'permission', 'project']


class IssueSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title', 'priority', 'project_id', 'author', 'assign']


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comments
        fields = ['id', 'desc', 'created_time', 'author', 'issue']


class ProjectDetailSerializer(ModelSerializer):
    contributors = ContributorSerializer(many=True, read_only=True)
    issues = IssueSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'desc', 'type', 'status', 'author', 'contributors', 'issues']


class IssueProjectSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title', 'desc', 'tag', 'priority', 'status', 'author', 'assign']


class CommentIssueSerializer(ModelSerializer):

    class Meta:
        model = Comments
        fields = ['desc', 'author', 'created_time']


class ProjectCreateSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['title', 'desc', 'type', 'status']


class ContributorCreateSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['user', 'permission', 'role']


class IssueCreateSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['title', 'desc', 'tag', 'priority', 'status']


class CommentCreateSerializer(ModelSerializer):

    class Meta:
        model = Comments
        fields = ['desc']
