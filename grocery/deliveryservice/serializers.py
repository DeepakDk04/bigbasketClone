from rest_framework.serializers import ModelSerializer
from customer.serializers import userModelCustomSerializer

from .models import DeliveryServicer, DeliveryServicerProfile


class DeliveryServicerProfileCreateSerializer(ModelSerializer):

    class Meta:
        model = DeliveryServicerProfile
        fields = ('id', 'user', 'age', 'contactno')


class DeliveryServicerProfileDetailSerializer(ModelSerializer):

    user = userModelCustomSerializer()

    class Meta:
        model = DeliveryServicerProfile
        fields = ('id', 'user', 'age', 'contactno')
        depth = 1


class DeliveryServicerProfileUpdateSerializer(ModelSerializer):

    user = userModelCustomSerializer()

    class Meta:
        model = DeliveryServicerProfile
        fields = ('id', 'user', 'age', 'contactno')
        depth = 1


class DeliveryServicerCreateSerializer(ModelSerializer):

    class Meta:
        model = DeliveryServicer
        fields = ('id', 'profile', 'ratings')


class DeliveryServicer__ProfileSerializer(ModelSerializer):

    user = userModelCustomSerializer()

    class Meta:
        model = DeliveryServicerProfile
        fields = '__all__'


class DeliveryServicerDetailSerializer(ModelSerializer):

    profile = DeliveryServicer__ProfileSerializer()

    class Meta:
        model = DeliveryServicer
        fields = ('id', 'profile', 'ratings')
        depth = 2


class DeliveryServicerUpdateSerializer(ModelSerializer):

    class Meta:
        model = DeliveryServicer
        fields = ('id', 'profile', 'ratings')
