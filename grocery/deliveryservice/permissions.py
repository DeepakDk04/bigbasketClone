from rest_framework.permissions import BasePermission


class IsOwnerDeliverProfile(BasePermission):
    """
    Object-level permission to only allow owners of an object to access it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.profile.user == request.user


class IsOwnerDeliver(BasePermission):
    """
    Object-level permission to only allow owners of an object to access it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user