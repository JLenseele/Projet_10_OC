from rest_framework.serializers import ModelSerializer
from .models import Project, Contributor, Issue, Comments


class ProjectSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'author', 'contributors']


class ContributorSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['user', 'id', 'role', 'permission', 'project']


class ContributorProjectSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['user', 'permission']


class ProjectDetailSerializer(ModelSerializer):

    contributor = ContributorSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'type', 'status', 'author', 'contributor']


class IssueSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title', 'priority', 'project_id', 'author', 'assign']


class IssueProjectSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title', 'desc', 'tag', 'priority', 'status', 'author', 'assign']


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comments
        fields = ['id', 'desc', 'created_time', 'author', 'issue']


class CommentIssueSerializer(ModelSerializer):

    class Meta:
        model = Comments
        fields = ['desc', 'author', 'issue', 'created_time']
