from customer.models import Customer
from rest_framework.permissions import BasePermission


class IsCustomerUser(BasePermission):
    """
    Object-level permission to only allow owners of an object to access it.
    Only Customer Account Holders can place order
    """

    def has_object_permission(self, request, view, obj):
        return request.user.groups.filter(name="Customer").exists()


class IsCartOwner(BasePermission):
    """
    Object-level permission to only allow owners of an object to access it.
    Only Customer  can updates his Cart , Check the cart id is the user's cart
    """

    def has_object_permission(self, request, view, obj):

        # customerprofile = request.user.customerprofile
        # cartID = Customer.objects.get(profile=customerprofile).cart.id

        return obj == request.user.customerprofile.customer.cart


class IsOrderShipper(BasePermission):
    '''
    Order Status can be updated only by the respective ordershipper
    '''

    def has_object_permission(self, request, view, obj):

        return obj.ordershipper == request.user.deliveryservicerprofile.deliveryservicer
