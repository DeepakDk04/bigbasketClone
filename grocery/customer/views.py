from rest_framework.generics import CreateAPIView, DestroyAPIView, RetrieveAPIView, UpdateAPIView

from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsOwnerProfile

from rest_framework.response import Response

# Create your views here.
from .models import Customer, CustomerProfile, DeliveryAddress

from .serializers import (

    ProfileCreateSerializer,
    ProfileViewSerializer,
    ProfileUpdateSerializer,
    ProfileDeleteSerializer,
    AddressCreateOrViewOrUpdateSerializer,
    CustomerCreateOrViewOrUpdateSerializer,

)


class CustomerProfileCreateView(CreateAPIView):
    '''
    Creates the customer Profile
    '''
    queryset = CustomerProfile.objects.all()
    serializer_class = ProfileCreateSerializer
    permission_classes = [IsAuthenticated]


class CustomerProfileDetailView(RetrieveAPIView):
    '''
    Displays the customer Profile
    '''
    queryset = CustomerProfile.objects.all()
    serializer_class = ProfileViewSerializer
    permission_classes = [IsAuthenticated]  # anybody looged in can view
    # permission_classes = [IsOwnerProfile] to make only the profile owners can view
    lookup_field = 'id'


class CustomerProfileUpdateView(UpdateAPIView):
    '''
    Updates the customer Profile
    '''
    queryset = CustomerProfile.objects.all()
    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAuthenticated]  # anybody looged in can view
    # permission_classes = [IsOwnerProfile] to make only the profile owners can view
    lookup_field = 'id'


class CustomerProfileDeleteView(DestroyAPIView):
    '''
    Deletes the customer Profile
    '''
    queryset = CustomerProfile.objects.all()
    serializer_class = ProfileDeleteSerializer
    permission_classes = [IsAuthenticated]  # anybody looged in can view
    # permission_classes = [IsOwnerProfile] to make only the profile owners can view
    lookup_field = 'id'
