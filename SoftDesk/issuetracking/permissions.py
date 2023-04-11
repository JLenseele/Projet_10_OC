from rest_framework.permissions import BasePermission
from .models import Project

EDIT_METHOD = ['DELETE', 'PUT', 'PATCH']
SAFE_METHOD = ['POST', 'GET']
READONLY = ['GET']


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
            return contributor_author_permission(request, view.kwargs["project_pk"])
        except KeyError:
            return False

    def has_object_permission(self, request, view, obj):
        print(request.method)
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


class IsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        try:
            # si project_pk est dans l'URL, on vérifie que l'user et
            # author ou contributeur du projet
            return contributor_author_permission(request, view.kwargs["project_pk"])
        except KeyError:
            try:
                return contributor_author_permission(request, view.kwargs["pk"])
            except KeyError:
                return bool(request.user.is_authenticated)
            # si project_pk n'existe pas dans l'URL on vérifie juste
            # que l'user est bien authentifié
            return bool(request.user.is_authenticated)


class IsAuthor(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        # Vérifie si l'user est l'auteur de l'objet (project/problem/commentaire)
        return bool(request.user.id == obj.author_id)


class IsContributor(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        # dans tous les cas, seuls les auteurs sont autorisés
        # à modifier/supprimer un objet
        if request.method in EDIT_METHOD:
            return False
        # On vérifie ensuite pour les méthodes GET / POST
        # si l'utilisateur est contributeur
        for contrib in obj.contributors.all():
            if contrib.user == request.user:
                return True
        return False


class IsAuthorContributor(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        return bool(int(view.kwargs["project_pk"]) == obj.project_id)


class IsContributorContributor(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        if request.method in EDIT_METHOD:
            return False
        project = view.kwargs["project_pk"]
        obj = Project.objects.filter(id=project).distinct()
        if not obj:
            return False
        for contrib in obj[0].contributors.all():
            if contrib.user == request.user:
                return True
            return False
