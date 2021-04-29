from django.contrib.auth.models import Group
from .models import DeliveryServicer, DeliveryServicerProfile

from rest_framework.permissions import AllowAny, IsAuthenticated

from .permissions import (

    IsOwnerDeliver,
    IsOwnerDeliverProfile,
    IsDeliverGroup,
    IsOrderedCustomer

)
from rest_framework import status
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

    # DeliveryServicerProfileDetailSerializer,
    DeliveryServicerProfileCreateSerializer,
    DeliveryServicerProfileUpdateSerializer,

    DeliveryServicerCreateSerializer,
    DeliveryServicerDetailSerializer,

    DeliveryServicerRatingsUpdateSerializer,
    DeliveryServicerDeliveryUpdateSerializer,
    DeliverServicerAvailableUpdateSerializer,
)


# Create your views here.
class DeliverServicerSignUpAPIView(GenericAPIView):

    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

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


# class DeliverServicerProfileCreateView(CreateAPIView):
#     '''
#     Creates the Delivery Servicer Profile
#     '''
#     queryset = DeliveryServicerProfile.objects.all()
#     serializer_class = DeliveryServicerProfileCreateSerializer
#     permission_classes = (IsAuthenticated, IsDeliverGroup)


# class DeliverServicerProfileDetailView(RetrieveAPIView):
#     '''
#     View Details of the Delivery Servicer Profile
#     '''
#     queryset = DeliveryServicerProfile.objects.all()
#     serializer_class = DeliveryServicerProfileDetailSerializer
#     permission_classes = (IsOwnerDeliverProfile,)
#     lookup_field = 'id'


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
    permission_classes = (IsAuthenticated, IsDeliverGroup)

    def create(self, request, *args, **kwargs):

        profile_serializer = DeliveryServicerProfileCreateSerializer(
            data=request.data)
        profile_serializer.is_valid(raise_exception=True)
        profile = profile_serializer.save()

        profile_data = {"profile": profile.id}

        deliverer_serializer = self.get_serializer(data=profile_data)
        deliverer_serializer.is_valid(raise_exception=True)
        deliverer_serializer.save()

        return Response(deliverer_serializer.data, status=status.HTTP_201_CREATED)


class DeliverServicerDetailView(RetrieveAPIView):
    '''
    View details of the Delivery Servicer
    '''
    queryset = DeliveryServicer.objects.all()
    serializer_class = DeliveryServicerDetailSerializer
    permission_classes = (IsOwnerDeliver,)
    lookup_field = 'id'


class DeliverServicerRatingsUpdateView(UpdateAPIView):
    '''
    Put ratings for Delivery Servicer by the Customer
    '''
    queryset = DeliveryServicer.objects.all()
    serializer_class = DeliveryServicerRatingsUpdateSerializer
    permission_classes = (IsAuthenticated, IsOrderedCustomer)
    lookup_field = 'id'


class DeliverServicerDeliveryUpdateView(UpdateAPIView):
    '''
    Update Delivery Status [placed->delivery->reached]
    of Order by the deliveryshipper
    '''
    queryset = DeliveryServicer.objects.all()
    serializer_class = DeliveryServicerDeliveryUpdateSerializer
    permission_classes = (IsOwnerDeliver,)
    lookup_field = 'id'


class DeliverServicerAvailableUpdateView(UpdateAPIView):
    '''
    Update active status of DelivererAccount
    by Deliverer Servicer himself
    [Active Deliverers only Recieve Orders to deliver]
    '''
    queryset = DeliveryServicer.objects.all()
    serializer_class = DeliverServicerAvailableUpdateSerializer
    permission_classes = (IsOwnerDeliver,)
    lookup_field = 'id'
