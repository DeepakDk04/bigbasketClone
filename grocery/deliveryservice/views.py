from django.contrib.auth.models import Group
from .models import DeliveryServicer, DeliveryServicerProfile

from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsOwnerDeliver, IsOwnerDeliverProfile

from rest_framework.generics import GenericAPIView
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)

from authentication.serializers import UserSerializer, RegisterSerializer
from rest_framework.response import Response
from knox.models import AuthToken

from .serializers import (

    DeliveryServicerProfileDetailSerializer,
    DeliveryServicerProfileCreateSerializer,
    DeliveryServicerProfileUpdateSerializer,

    DeliveryServicerCreateSerializer,
    DeliveryServicerDetailSerializer,
    DeliveryServicerUpdateSerializer,
)


# Create your views here.
class DeliverServicerSignUpAPIView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        group = Group.objects.get(name='Deliveryservicer')
        user.groups.add(group)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


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
