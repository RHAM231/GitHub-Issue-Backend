from rest_framework import permissions


class MyPermission(permissions.BasePermission):

    def __init__(self, allowed_methods):
        super().__init__()
        self.allowed_methods = allowed_methods

    def has_permission(self, request, view):
        return request.method in self.allowed_methods


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user