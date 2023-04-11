from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from authentication.models import User
from .permissions import IsAuthenticated, \
    IsProjectAuthorContributor, \
    IsObjectAuthor
from .models import Project, \
    Contributor, \
    Issue, \
    Comments
from .serializers import ProjectSerializer, \
    ProjectDetailSerializer, \
    ContributorSerializer, ContributorProjectSerializer, \
    IssueSerializer, IssueProjectSerializer, \
    CommentSerializer, CommentIssueSerializer


class ProjectViewset(ModelViewSet):

    serializer_class = ProjectSerializer
    detail_serializer_class = ProjectDetailSerializer
    permission_classes = [IsProjectAuthorContributor | IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Project.objects.filter(
            Q(author=user.id) |
            Q(contributors__user=user)
        ).distinct()
        return queryset

    def get_serializer_class(self):
        actions = ['retrieve', 'create', 'update']
        if self.action in actions:
            return self.detail_serializer_class
        return super().get_serializer_class()


class ContributorViewset(ModelViewSet):

    serializer_class = ContributorSerializer
    permission_classes = [IsProjectAuthorContributor]

    def get_queryset(self):
        return Contributor.objects.filter(project_id=self.kwargs["project_pk"])

    def create(self, request, *args, **kwargs):
        serializer = ContributorProjectSerializer(data=request.data)
        project = Project.objects.get(id=self.kwargs['project_pk'])
        user = User.objects.get(id=request.data["user"])
        permission = request.data["permission"]
        if serializer.is_valid():
            serializer.save(
                project_id=project.id,
                user_id=user.id,
                role="CO",
                permission=permission,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_200_OK)


class IssueViewset(ModelViewSet):

    serializer_class = IssueSerializer
    detail_serializer_class = IssueProjectSerializer
    permission_classes = [IsObjectAuthor]

    def get_queryset(self):
        return Issue.objects.filter(project_id=self.kwargs["project_pk"])

    def get_serializer_class(self):
        actions = ['retrieve', 'create', 'update']
        if self.action in actions:
            return self.detail_serializer_class
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = IssueProjectSerializer(data=request.data)
        project = Project.objects.get(id=self.kwargs['project_pk'])
        user = self.request.user
        if serializer.is_valid():
            serializer.save(
                project_id=project,
                author=user,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_200_OK)


class CommentViewset(ModelViewSet):

    serializer_class = CommentSerializer
    detail_serializer_class = CommentIssueSerializer
    permission_classes = [IsProjectAuthorContributor | IsObjectAuthor]

    def get_queryset(self):
        return Comments.objects.filter(issue=self.kwargs["issue_pk"])

    def get_serializer_class(self):
        actions = ['retrieve', 'create', 'update']
        if self.action in actions:
            return self.detail_serializer_class
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = CommentIssueSerializer(data=request.data)
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
