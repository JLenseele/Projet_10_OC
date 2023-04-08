from rest_framework.permissions import BasePermission
from .models import Project


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
    project = Project.objects.filter(id=project_id).disctinct()
    if author_permission(request, project):
        return True
    if contributor_permission(request, project):
        return True
    return False


class IsAuthenticated(BasePermission):

    def has_permission(self, request, view):

        try:
            # si project_pk est dans l'URL, on vérifie que l'user et
            # author ou contributeur du projet
            return contributor_author_permission(request, view.kwargs["project_pk"])
        except KeyError:
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
        if request.method in ['DELETE', 'PUT', 'PATCH']:
            return False
        # On vérifie ensuite pour les method GET / POST
        # si l'utilisateur est contributeur
        for contrib in obj.contributors.all():
            if contrib.user == request.user:
                print('contrib OK')
                return True
            return False


class IsAssigned(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        if request.method in ['DELETE', 'PUT', 'PATCH']:
            return False
        return bool(request.user == obj.assign)


class IsAuthorContributor(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        return bool(int(view.kwargs["project_pk"]) == int(obj.project_id))


class IsContributorContributor(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        if request.method in ['DELETE', 'PUT', 'PATCH', 'POST']:
            return False
        project = view.kwargs["project_pk"]
        obj = Project.objects.filter(id=project).distinct()
        if not obj:
            return False
        for contrib in obj[0].contributors.all():
            if contrib.user == request.user:
                return True
            return False
