from rest_framework.serializers import ModelSerializer
from customer.serializers import userModelCustomSerializer

from .models import DeliveryServicer, DeliveryServicerProfile


class DeliveryServicerProfileCreateSerializer(ModelSerializer):

    class Meta:
        model = DeliveryServicerProfile
        fields = ('id', 'user', 'age', 'gender', 'contactno')


# class DeliveryServicerProfileDetailSerializer(ModelSerializer):

#     user = userModelCustomSerializer()

#     class Meta:
#         model = DeliveryServicerProfile
#         fields = ('id', 'user', 'age', 'gender', 'contactno')
#         depth = 1


class DeliveryServicerProfileUpdateSerializer(ModelSerializer):

    user = userModelCustomSerializer()

    class Meta:
        model = DeliveryServicerProfile
        fields = ('id', 'user', 'age', 'gender', 'contactno')
        depth = 1


class DeliveryServicer__ProfileSerializer(ModelSerializer):

    user = userModelCustomSerializer()

    class Meta:
        model = DeliveryServicerProfile
        fields = '__all__'


class DeliveryServicerCreateSerializer(ModelSerializer):

    class Meta:
        model = DeliveryServicer
        fields = ('id', 'profile')


class DeliveryServicerDetailSerializer(ModelSerializer):

    profile = DeliveryServicer__ProfileSerializer()

    class Meta:
        model = DeliveryServicer
        fields = ('id', 'profile', 'ratings', 'mydeliveries')
        depth = 2


class DeliveryServicerRatingsUpdateSerializer(ModelSerializer):

    class Meta:
        model = DeliveryServicer
        fields = ('id', 'ratings')


class DeliveryServicerDeliveryUpdateSerializer(ModelSerializer):

    class Meta:
        model = DeliveryServicer
        fields = ('id', 'mydeliveries')


class DeliverServicerAvailableUpdateSerializer(ModelSerializer):

    class Meta:
        model = DeliveryServicer
        fields = ('id', 'available')
