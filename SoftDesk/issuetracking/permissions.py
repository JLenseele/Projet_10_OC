from rest_framework.permissions import BasePermission
from .models import Project

EDIT_METHOD = ['DELETE', 'PUT', 'PATCH']
SAFE_METHOD = ['POST', 'GET']


class IsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated)


class IsProjectAuthorContributor(IsAuthenticated):

    def has_permission(self, request, view):
        try:
            return contributor_author_permission(request, view.kwargs["project_pk"])
        except KeyError:
            try:
                return contributor_author_permission(request, view.kwargs["pk"])
            except KeyError:
                return False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsObjectAuthor(IsProjectAuthorContributor):

    def has_permission(self, request, view):
        print(request.method)
        try:
            return contributor_author_object_permission(request, view.kwargs["project_pk"])
        except KeyError:
            return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHOD:
            return True
        return bool(request.user == obj.author)


def author_permission(request, obj):
    if not obj:
        return False
    if request.user == obj.author:
        return True


def contributor_permission(request, obj):
    if not obj:
        return False
    for contrib in obj.contributors.all():
        if contrib.user == request.user:
            return True
    return False


def contributor_author_permission(request, project_id):
    project = Project.objects.filter(id=project_id).distinct()
    if project:
        if author_permission(request, project[0]):
            return True
        if contributor_permission(request, project[0])\
                and request.method in SAFE_METHOD:
            return True
    return False


def contributor_author_object_permission(request, project_id):
    project = Project.objects.filter(id=project_id).distinct()
    if project:
        if author_permission(request, project[0]):
            return True
        if contributor_permission(request, project[0]):
            return True
    return False
