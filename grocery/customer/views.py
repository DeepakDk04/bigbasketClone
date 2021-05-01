
from products.models import Product
from order.models import Cart, CartItem, Order
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .permissions import IsOwnerProfile, IsOwnerCustomer, IsOwnerUser, IsCustomerOwnsOrder


from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)

from rest_framework import status
from .models import Customer, CustomerProfile, DeliveryAddress

from .serializers import (

    CustomerCreateOrUpdateSerializer,
    CustomerViewSerializer,
    CustomerDeleteSerializer,

    ProfileCreateSerializer,
    # ProfileViewSerializer,
    userModelCustomSerializer,
    ProfileUpdateSerializer,
    # ProfileDeleteSerializer,

    AddressCreateOrViewOrUpdateSerializer,
    # AddressDeleteSerializer,
    CustomerUpdateCustomSerializer,
    CustomerPlacedOrdersSerializer,

)

# Create your views here.


# class CustomerProfileCreateView(CreateAPIView):
#     '''
#     Creates the customer Profile
#     '''
#     queryset = CustomerProfile.objects.all()
#     serializer_class = ProfileCreateSerializer
#     permission_classes = (IsAuthenticated,)


# class CustomerProfileDetailView(RetrieveAPIView):
#     '''
#     Displays the customer Profile
#     '''
#     queryset = CustomerProfile.objects.all()
#     serializer_class = ProfileViewSerializer
#     permission_classes = (IsOwnerProfile,)
#     lookup_field = 'id'


class UserUpdateView(UpdateAPIView):
    '''
    Updates the customer Profile
    '''
    queryset = User.objects.all()
    serializer_class = userModelCustomSerializer
    permission_classes = (IsOwnerUser, IsAuthenticated)
    lookup_field = 'id'


# class CustomerProfileUpdateView(UpdateAPIView):
#     '''
#     Updates the customer Profile
#     '''
#     queryset = CustomerProfile.objects.all()
#     serializer_class = ProfileUpdateSerializer
#     permission_classes = (IsOwnerProfile,)
#     lookup_field = 'id'


# class CustomerProfileDeleteView(DestroyAPIView):
#     '''
#     Deletes the customer Profile,
#     Note: ( Bad Practice to delete a profile, better avoid, it affects customer table )
#     '''
#     queryset = CustomerProfile.objects.all()
#     serializer_class = ProfileDeleteSerializer
#     permission_classes = (IsOwnerProfile,)
#     lookup_field = 'id'


# class AddressCreateView(CreateAPIView):
#     '''
#     Creates the customer Address
#     '''
#     queryset = DeliveryAddress.objects.all()
#     serializer_class = AddressCreateOrViewOrUpdateSerializer
#     permission_classes = (IsAuthenticated,)


# class AddressDetailView(RetrieveAPIView):
#     '''
#     Get address of the customer
#     '''
#     queryset = DeliveryAddress.objects.all()
#     serializer_class = AddressCreateOrViewOrUpdateSerializer
#     permission_classes = (IsAuthenticated,)
#     lookup_field = 'id'


# class AddressUpdateView(UpdateAPIView):
#     '''
#     update address of the customer
#     '''
#     queryset = DeliveryAddress.objects.all()
#     serializer_class = AddressCreateOrViewOrUpdateSerializer
#     permission_classes = (IsAuthenticated,)
#     lookup_field = 'id'


# class AddressDeleteView(DestroyAPIView):
#     '''
#     delete address of the customer
#     '''
#     queryset = DeliveryAddress.objects.all()
#     serializer_class = AddressDeleteSerializer
#     permission_classes = (IsAuthenticated,)
#     lookup_field = 'id'


class CustomerCreateView(CreateAPIView):
    '''
    Creates the Customer
    '''
    queryset = Customer.objects.all()
    serializer_class = CustomerCreateOrUpdateSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        """ 
        Overrided Create() method for nested [Profile, Address, Cart] Creations.
        """

        profileData = request.data.get("profile")
        addressData = request.data.get("address")

        if not profileData or not addressData:
            errorMessage = {"field_error": {
                "profile, address": "required fields"}}
            return Response(data=errorMessage, status=status.HTTP_400_BAD_REQUEST)

        profile_create_serializer = ProfileCreateSerializer(data=profileData)
        profile_create_serializer.is_valid(raise_exception=True)
        profile = profile_create_serializer.save()

        address_create_serializer = AddressCreateOrViewOrUpdateSerializer(
            data=addressData)
        address_create_serializer.is_valid(raise_exception=True)
        address = address_create_serializer.save()

        emptycart = Cart.objects.create()

        customerAccountData = {}
        customerAccountData["profile"] = profile.id
        # ''' manytomany field expects list of pk (adddres field) '''
        customerAccountData["address"] = [address.id]
        customerAccountData["cart"] = emptycart.id

        serializer = self.get_serializer(data=customerAccountData)
        serializer.is_valid(raise_exception=True)
        customer = serializer.save()

        customer_response = CustomerViewSerializer(customer).data

        return Response(customer_response, status=status.HTTP_201_CREATED)


class CustomerDetailView(RetrieveAPIView):
    '''
    Get Customer Details
    '''
    queryset = Customer.objects.all()
    serializer_class = CustomerViewSerializer
    permission_classes = (IsOwnerCustomer,)
    lookup_field = 'id'


class CustomerUpdateView(UpdateAPIView):
    '''
    Update Customer Details
    '''
    queryset = Customer.objects.all()
    serializer_class = CustomerUpdateCustomSerializer
    permission_classes = (IsOwnerCustomer,)
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        """ 
        Overrided Update() method for nested [Profile, Address, User] updates.
        """

        instance = self.get_object()
        customer_update_serializer = self.get_serializer_class()

        requestdata = request.data
        profile_data = requestdata.get("profile", False)
        addresses_list_data = requestdata.get("address", False)

        if profile_data:
            ''' Handles Updates of Customer Profile instance '''

            user_data = profile_data.get("user", False)

            if user_data:
                ''' Handles Updates of user instance '''
                user_instance = instance.profile.user
                new_username = user_data.get('username')

                if new_username != user_instance.username and User.objects.filter(username=new_username).exists():
                    errorMessage = {"username": "not available"}
                    return Response(data=errorMessage, status=status.HTTP_400_BAD_REQUEST)

                if new_username == user_instance.username:
                    ''' Since same username can't be saved anothertime, violates unique property '''
                    user_data.pop("username")

                user_serializer = userModelCustomSerializer(
                    user_instance, data=user_data, partial=True)

                user_serializer.is_valid(raise_exception=True)
                user_serializer.save()
                #  if "user" remains in request, it clashes when profile updating
                profile_data.pop("user")

            profile_instance = instance.profile

            profile_serializer = ProfileUpdateSerializer(
                profile_instance, data=profile_data, partial=True)

            profile_serializer.is_valid(raise_exception=True)
            profile_serializer.save()

        if addresses_list_data:
            ''' Handles Updates of Customer Address instance '''

            for address in addresses_list_data:
                ''' Iterate Over Each Addresses '''

                address_id = address.get("id", False)
                doorno_data = address.get("doorno", False)
                street_data = address.get("street", False)
                area_data = address.get("area", False)
                landmark_data = address.get("landmark", False)

                if not (doorno_data and street_data and area_data and landmark_data):
                    errorMessage = {
                        "required_fields": "doorno,street,area,landmark"}
                    return Response(data=errorMessage, status=status.HTTP_400_BAD_REQUEST)

                if address_id:
                    ''' already exist addresses , needs to updated'''

                    if not DeliveryAddress.objects.filter(id=address_id).exists():
                        errorMessage = {"field_error": "address id not valid"}
                        return Response(data=errorMessage, status=status.HTTP_400_BAD_REQUEST)

                    address_instance = DeliveryAddress.objects.get(
                        id=address_id)
                    updated_address_serializer = AddressCreateOrViewOrUpdateSerializer(
                        address_instance, data=address, partial=True)

                    updated_address_serializer.is_valid(raise_exception=True)
                    updated_address_serializer.save()

                else:
                    ''' creates new address instance and add to the customer instance '''
                    new_address_serializer = AddressCreateOrViewOrUpdateSerializer(
                        data=address)

                    new_address_serializer.is_valid(raise_exception=True)
                    new_address = new_address_serializer.save()

                    instance.address.add(new_address)

        customer_response = customer_update_serializer(instance).data

        return Response(customer_response, status=status.HTTP_201_CREATED)


class CustomerDeleteView(DestroyAPIView):
    '''
    Delete Customer Details
    '''
    queryset = Customer.objects.all()
    serializer_class = CustomerDeleteSerializer
    permission_classes = (IsOwnerCustomer,)
    lookup_field = 'id'


class CustomerPlacedOrdersProgressView(RetrieveAPIView):
    ''' get the current placed orders in process '''

    queryset = Customer.objects.all()
    serializer_class = CustomerPlacedOrdersSerializer
    permission_classes = (IsOwnerCustomer,)
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):

        customer = self.get_object()
        allorders = customer.myorders.all()
        orders = allorders.exclude(status="reached").exclude(
            status="cancelled").exclude(status="notplaced")

        if orders.exists():
            orderResponse = self.get_serializer(orders, many=True).data
            return Response(orderResponse, status=status.HTTP_200_OK)

        return Response({"order": "no order processing"}, status=status.HTTP_204_NO_CONTENT)
