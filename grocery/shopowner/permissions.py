from rest_framework.permissions import BasePermission


class IsOwnerGroup(BasePermission):
    """
    Object-level permission to only allow owners of an object to access it.
    Only A user in a Shopowner group only can Access.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.groups.filter(name="Shopowner").exists()


class IsOwnerDetail(BasePermission):
    """
    Object-level permission to only allow owners of an object to access it.
    Only A user in a Shopowner  only can Access his own details account.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user.shopowner


class IsOwnerJoinCode(BasePermission):
    """
    Only the owner who generated the joincode can make invalidate it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.createdby == request.user.shopowner
