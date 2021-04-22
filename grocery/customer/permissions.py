from rest_framework.permissions import BasePermission


class IsOwnerProfile(BasePermission):
    """
    Object-level permission to only allow owners of an object to access it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
