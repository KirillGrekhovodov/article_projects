from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if view.action == "get_comments":
            return request.user.is_authenticated
        if request.user.is_authenticated and request.user == obj.author:
            return True
        return False