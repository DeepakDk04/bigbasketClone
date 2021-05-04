from rest_framework.generics import (

    GenericAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)

from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import (

    IsOwnerDeliver,
    IsDeliverGroup,
    IsOrderedCustomer

)

from django.contrib.auth.models import User, Group
from knox.models import AuthToken
from .models import DeliveryServicer


from authentication.serializers import UserSerializer, RegisterSerializer
from customer.serializers import userModelCustomSerializer
from .serializers import (


    DeliveryServicerProfileCreateSerializer,
    DeliveryServicerProfileUpdateSerializer,

    DeliveryServicerCreateSerializer,
    DeliveryServicerUpdateSerializer,
    DeliveryServicerDetailSerializer,

    DeliveryServicerRatingsUpdateSerializer,
    DeliverServicerAvailableUpdateSerializer,

    CheckOrderGiven__OrderSerializer,

)


from rest_framework.response import Response
from rest_framework import status


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
        deliveryServicer = deliverer_serializer.save()

        deliverer_response = DeliveryServicerDetailSerializer(
            deliveryServicer).data

        return Response(deliverer_response, status=status.HTTP_201_CREATED)


class DeliverServicerDetailView(RetrieveAPIView):
    '''
    View details of the Delivery Servicer
    '''
    queryset = DeliveryServicer.objects.all()
    serializer_class = DeliveryServicerDetailSerializer
    permission_classes = (IsAuthenticated, IsOwnerDeliver,)
    lookup_field = 'id'


class DeliverServicerUpdateView(UpdateAPIView):
    '''
    Update Details of the Delivery Servicer Profile
    '''
    queryset = DeliveryServicer.objects.all()
    serializer_class = DeliveryServicerUpdateSerializer
    permission_classes = (IsAuthenticated, IsOwnerDeliver,)
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        """ 
        Overrided Update() method for nested [Profile, User] updates.
        """

        deliverer = self.get_object()
        deliverer_update_serializer = self.get_serializer_class()

        profile_data = request.data.get("profile", False)

        if profile_data:
            ''' Handles Updates of DeliveryServicer Profile instance '''

            user_data = profile_data.get("user", False)

            if user_data:
                ''' Handles Updates of user instance '''
                user_instance = deliverer.profile.user
                old_username = user_instance.username
                new_username = user_data.get('username', False)

                if new_username:
                    if User.objects.exclude(username=old_username).filter(username=new_username).exists():
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

            if profile_data:
                ''' Handles Updates of profile instance other than user attribute'''
                profile_instance = deliverer.profile
                profile_serializer = DeliveryServicerProfileUpdateSerializer(
                    profile_instance, data=profile_data, partial=True)

                profile_serializer.is_valid(raise_exception=True)
                profile_serializer.save()

        deliverrer_response = deliverer_update_serializer(deliverer).data

        return Response(deliverrer_response, status=status.HTTP_202_ACCEPTED)


class DeliverServicerRatingsUpdateView(UpdateAPIView):
    '''
    Put ratings for Delivery Servicer by the Ordered Customer
    '''
    queryset = DeliveryServicer.objects.all()
    serializer_class = DeliveryServicerRatingsUpdateSerializer
    permission_classes = (IsAuthenticated, IsOrderedCustomer)
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):

        reqRating = request.data.get("ratings")

        if reqRating not in [0, 1, 2, 3, 4, 5]:
            errorMessage = {"status": "must be a number from 0 to 5"}
            return Response(data=errorMessage, status=status.HTTP_400_BAD_REQUEST)

        deliverer = self.get_object()
        oldRating = deliverer.ratings
        newRating = (reqRating + oldRating) // 2
        updatedData = {"ratings": newRating}
        serializer = self.get_serializer_class()
        serializer(deliverer, data=updatedData, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data={"status": "updated successfully"}, status=status.HTTP_202_ACCEPTED)


class DeliverServicerAvailableUpdateView(UpdateAPIView):
    '''
    Update active status of DelivererAccount
    by Deliverer Servicer himself
    [Active Deliverers only Recieve Orders to deliver]
    '''
    queryset = DeliveryServicer.objects.all()
    serializer_class = DeliverServicerAvailableUpdateSerializer
    permission_classes = (IsAuthenticated, IsOwnerDeliver,)
    lookup_field = 'id'


class CheckOrderGivenView(RetrieveAPIView):
    '''
    Checks If any order placed for the respective deliverer
    '''
    queryset = DeliveryServicer.objects.all()
    serializer_class = CheckOrderGiven__OrderSerializer
    permission_classes = (IsAuthenticated, IsOwnerDeliver,)
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        ''' get the placed orders '''
        deliverer = self.get_object()
        new_orders = deliverer.mydeliveries.all().exclude(status="reached").exclude(
            status="cancelled").exclude(status="notplaced")

        if new_orders.exists():
            order_response = self.get_serializer(new_orders, many=True).data
            return Response(order_response, status=status.HTTP_200_OK)
        else:
            message = {"order": "no order placed"}
            return Response(data=message, status=status.HTTP_204_NO_CONTENT)
