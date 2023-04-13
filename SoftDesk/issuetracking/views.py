from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ..authentication.models import User
from .permissions import IsAuthenticated, \
    IsProjectAuthorContributor, \
    IsObjectAuthor
from .models import Project, \
    Contributor, \
    Issue, \
    Comments
from .serializers import ProjectSerializer, \
    ProjectDetailSerializer, ProjectCreateSerializer, \
    ContributorSerializer, ContributorCreateSerializer, \
    IssueSerializer, IssueProjectSerializer, IssueCreateSerializer, \
    CommentSerializer, CommentIssueSerializer, CommentCreateSerializer


class ProjectViewset(ModelViewSet):

    serializer_class = ProjectSerializer
    detail_serializer_class = ProjectDetailSerializer
    create_serializer_class = ProjectCreateSerializer
    permission_classes = [IsProjectAuthorContributor | IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Project.objects.filter(
            Q(author=user.id) |
            Q(contributors__user=user)
        ).distinct()
        return queryset

    def get_serializer_class(self):
        actions = ['retrieve', 'update']
        if self.action in actions:
            return self.detail_serializer_class
        if self.action == 'create':
            return self.create_serializer_class
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = ProjectCreateSerializer(data=request.data)
        user = self.request.user
        if serializer.is_valid():
            serializer.save(
                author=user,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_200_OK)


class ContributorViewset(ModelViewSet):

    serializer_class = ContributorSerializer
    create_serializer_class = ContributorCreateSerializer
    permission_classes = [IsProjectAuthorContributor]

    def get_queryset(self):
        return Contributor.objects.filter(project_id=self.kwargs["project_pk"])

    def get_serializer_class(self):
        actions = ['update', 'create']
        if self.action in actions:
            return self.create_serializer_class
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = ContributorCreateSerializer(data=request.data)
        project = Project.objects.get(id=self.kwargs['project_pk'])
        user = User.objects.get(id=request.data["user"])
        if serializer.is_valid():
            serializer.save(
                project_id=project.id,
                user_id=user.id,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_200_OK)


class IssueViewset(ModelViewSet):

    serializer_class = IssueSerializer
    detail_serializer_class = IssueProjectSerializer
    create_serializer_class = IssueCreateSerializer
    permission_classes = [IsObjectAuthor]

    def get_queryset(self):
        return Issue.objects.filter(project_id=self.kwargs["project_pk"])

    def get_serializer_class(self):
        actions = ['retrieve', 'update']
        if self.action in actions:
            return self.detail_serializer_class
        if self.action == 'create':
            return self.create_serializer_class
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = IssueCreateSerializer(data=request.data)
        project = Project.objects.get(id=self.kwargs['project_pk'])
        user = self.request.user
        if serializer.is_valid():
            serializer.save(
                project_id=project,
                author=user,
                assign=user,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_200_OK)


class CommentViewset(ModelViewSet):

    serializer_class = CommentSerializer
    detail_serializer_class = CommentIssueSerializer
    create_serializer_class = CommentCreateSerializer
    permission_classes = [IsObjectAuthor]

    def get_queryset(self):
        issues = Issue.objects.filter(project_id=self.kwargs["project_pk"])
        for issue in issues:
            print(issue.id)
            if issue.id == int(self.kwargs["issue_pk"]):
                return Comments.objects.filter(issue=self.kwargs["issue_pk"])
        return

    def get_serializer_class(self):
        actions = ['retrieve', 'update']
        if self.action in actions:
            return self.detail_serializer_class
        if self.action == 'create':
            return self.create_serializer_class
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = CommentCreateSerializer(data=request.data)
        issue = Issue.objects.get(id=self.kwargs['issue_pk'])
        user = self.request.user
        if serializer.is_valid():
            serializer.save(
                issue=issue,
                author=user,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_200_OK)
