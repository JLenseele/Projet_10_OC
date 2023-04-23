from rest_framework.permissions import BasePermission


class SelfAccount(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return False
        return True

    def has_object_permission(self, request, view, obj):
        return True
