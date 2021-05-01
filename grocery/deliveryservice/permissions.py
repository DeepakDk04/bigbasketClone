from rest_framework.permissions import BasePermission


class IsOwnerDeliver(BasePermission):
    """
    Object-level permission to only allow owners of an object to access it.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user.deliveryservicerprofile.deliveryservicer


class IsOwnerDeliverProfile(BasePermission):
    """
    Object-level permission to only allow owners of an object to access it.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user.deliveryservicerprofile


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

        deliveries = obj.mydeliveries.all()
        customer = request.user.customerprofile.customer

        return deliveries.filter(orderbycustomer=customer).exists()

        # for order in deliveries:
        #     if order.orderbycustomer == request.user.customerprofile.customer:
        #         return True

        # return False
