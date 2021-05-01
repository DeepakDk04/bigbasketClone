from rest_framework.permissions import BasePermission


class IsOwnerProfile(BasePermission):
    """
    Object-level permission to only allow owners of an object to access it.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user.customerprofile


class IsOwnerCustomer(BasePermission):
    """
    Object-level permission to only allow owners of an object to access it.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user.customerprofile.customer


class IsOwnerUser(BasePermission):
    """
    Object-level permission to only allow owners of an object to access it.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsCustomerOwnsOrder(BasePermission):
    """
    Object-level permission to only allow owners of an object to access it.
    """

    def has_object_permission(self, request, view, obj):
        allOrders = request.user.customerprofile.customer.myorders.all()

        return allOrders.filter(id=obj.id).exists()
