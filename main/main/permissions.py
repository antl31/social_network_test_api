from rest_framework import permissions


class IsAnonCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True

        elif request.user.is_anonymous and request.method != "POST":
            return False
        elif request.method in permissions.SAFE_METHODS:
            return True