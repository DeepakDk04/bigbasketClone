
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsOwnerProfile, IsOwnerCustomer, IsOwnerUser


from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)

from .models import Customer, CustomerProfile, DeliveryAddress

from .serializers import (

    CustomerCreateOrUpdateSerializer,
    CustomerViewSerializer,
    CustomerDeleteSerializer,

    ProfileCreateSerializer,
    ProfileViewSerializer,
    userModelCustomSerializer,
    ProfileUpdateSerializer,
    ProfileDeleteSerializer,

    AddressCreateOrViewOrUpdateSerializer,
    AddressDeleteSerializer,

)

# Create your views here.


class CustomerProfileCreateView(CreateAPIView):
    '''
    Creates the customer Profile
    '''
    queryset = CustomerProfile.objects.all()
    serializer_class = ProfileCreateSerializer
    permission_classes = (IsAuthenticated,)


class CustomerProfileDetailView(RetrieveAPIView):
    '''
    Displays the customer Profile
    '''
    queryset = CustomerProfile.objects.all()
    serializer_class = ProfileViewSerializer
    permission_classes = (IsOwnerProfile,)
    lookup_field = 'id'


class UserUpdateView(UpdateAPIView):
    '''
    Updates the customer Profile
    '''
    queryset = User.objects.all()
    serializer_class = userModelCustomSerializer
    permission_classes = (IsOwnerUser, IsAuthenticated)
    lookup_field = 'id'


class CustomerProfileUpdateView(UpdateAPIView):
    '''
    Updates the customer Profile
    '''
    queryset = CustomerProfile.objects.all()
    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsOwnerProfile]
    lookup_field = 'id'


class CustomerProfileDeleteView(DestroyAPIView):
    '''
    Deletes the customer Profile, 
    Note: ( Bad Practice to delete a profile, better avoid, it affects customer table )
    '''
    queryset = CustomerProfile.objects.all()
    serializer_class = ProfileDeleteSerializer
    permission_classes = (IsOwnerProfile,)
    lookup_field = 'id'


class AddressCreateView(CreateAPIView):
    '''
    Creates the customer Address
    '''
    queryset = DeliveryAddress.objects.all()
    serializer_class = AddressCreateOrViewOrUpdateSerializer
    permission_classes = (IsAuthenticated,)


class AddressDetailView(RetrieveAPIView):
    '''
    Get address of the customer
    '''
    queryset = DeliveryAddress.objects.all()
    serializer_class = AddressCreateOrViewOrUpdateSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'


class AddressUpdateView(UpdateAPIView):
    '''
    update address of the customer
    '''
    queryset = DeliveryAddress.objects.all()
    serializer_class = AddressCreateOrViewOrUpdateSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'


class AddressDeleteView(DestroyAPIView):
    '''
    delete address of the customer
    '''
    queryset = DeliveryAddress.objects.all()
    serializer_class = AddressDeleteSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'


class CustomerCreateView(CreateAPIView):
    '''
    Creates the Customer
    '''
    queryset = Customer.objects.all()
    serializer_class = CustomerCreateOrUpdateSerializer
    permission_classes = (IsAuthenticated,)


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
    serializer_class = CustomerCreateOrUpdateSerializer
    permission_classes = (IsOwnerCustomer,)
    lookup_field = 'id'


class CustomerDeleteView(DestroyAPIView):
    '''
    Delete Customer Details
    '''
    queryset = Customer.objects.all()
    serializer_class = CustomerDeleteSerializer
    permission_classes = (IsOwnerCustomer,)
    lookup_field = 'id'
