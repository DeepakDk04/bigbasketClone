from rest_framework.permissions import BasePermission


class IsOwnerDeliver(BasePermission):
    """
    Object-level permission to only allow owners of an object to access it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.profile.user == request.user


class IsOwnerDeliverProfile(BasePermission):
    """
    Object-level permission to only allow owners of an object to access it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsDeliverGroup(BasePermission):
    """
    Object-level permission to only allow owners of an object to access it.
    Only A user in a deliverservicer group can create the deliverservicer account.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.groups.filter(name="Deliveryservicer").exists()


class IsOrderedCustomer(BasePermission):
    """
    Object-level permission to only allow owners of an object to access it.
    Only the customer who placed order and recieved from the delivery guy can tell ratings of delivery servicer.
    """

    def has_object_permission(self, request, view, obj):

        deliveries = list(obj.mydeliveries.all())

        for order in deliveries:
            if order.orderbycustomer.profile.user == request.user:
                return True

        return False
