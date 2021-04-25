from .models import DeliveryServicer, DeliveryServicerProfile

from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsOwnerDeliver, IsOwnerDeliverProfile

from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)

from .serializers import (

    DeliveryServicerProfileDetailSerializer,
    DeliveryServicerProfileCreateSerializer,
    DeliveryServicerProfileUpdateSerializer,

    DeliveryServicerCreateSerializer,
    DeliveryServicerDetailSerializer,
    DeliveryServicerUpdateSerializer,
)


# Create your views here.

class DeliverServicerProfileCreateView(CreateAPIView):
    '''
    Creates the Delivery Servicer Profile
    '''
    queryset = DeliveryServicerProfile.objects.all()
    serializer_class = DeliveryServicerProfileCreateSerializer
    permission_classes = (IsAuthenticated,)


class DeliverServicerProfileDetailView(RetrieveAPIView):
    '''
    View Details of the Delivery Servicer Profile
    '''
    queryset = DeliveryServicerProfile.objects.all()
    serializer_class = DeliveryServicerProfileDetailSerializer
    permission_classes = (IsOwnerDeliverProfile,)
    lookup_field = 'id'


class DeliverServicerProfileUpdateView(UpdateAPIView):
    '''
    Update Details of the Delivery Servicer Profile
    '''
    queryset = DeliveryServicerProfile.objects.all()
    serializer_class = DeliveryServicerProfileUpdateSerializer
    permission_classes = (IsOwnerDeliverProfile,)
    lookup_field = 'id'


class DeliverServicerCreateView(CreateAPIView):
    '''
    Creates the Delivery Servicer Account
    '''
    queryset = DeliveryServicer.objects.all()
    serializer_class = DeliveryServicerCreateSerializer
    permission_classes = (IsAuthenticated,)


class DeliverServicerDetailView(RetrieveAPIView):
    '''
    View details of the Delivery Servicer
    '''
    queryset = DeliveryServicer.objects.all()
    serializer_class = DeliveryServicerDetailSerializer
    permission_classes = (IsOwnerDeliver,)
    lookup_field = 'id'


class DeliverServicerUpdateView(UpdateAPIView):
    '''
    Update details of the Delivery Servicer Account
    '''
    queryset = DeliveryServicer.objects.all()
    serializer_class = DeliveryServicerUpdateSerializer
    permission_classes = (IsOwnerDeliver,)
    lookup_field = 'id'
