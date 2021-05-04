from django.contrib.auth.models import User
from products.models import Product
from rest_framework.serializers import ModelSerializer
from customer.serializers import userModelCustomSerializer

from .models import DeliveryServicer, DeliveryServicerProfile
from order.models import Order, OrderItem
from customer.models import Customer, CustomerProfile, DeliveryAddress


class DeliveryServicerProfileCreateSerializer(ModelSerializer):
    # used in
    class Meta:
        model = DeliveryServicerProfile
        fields = ('id', 'user', 'age', 'gender', 'contactno')


class DeliveryServicerProfileUpdateSerializer(ModelSerializer):

    class Meta:
        model = DeliveryServicerProfile
        fields = "__all__"


class DeliveryServicer__ProfileSerializer(ModelSerializer):

    user = userModelCustomSerializer()

    class Meta:
        model = DeliveryServicerProfile
        fields = '__all__'


class DeliveryServicerCreateSerializer(ModelSerializer):

    class Meta:
        model = DeliveryServicer
        fields = ('id', 'profile')


class MyDeliveries_ToaddressSerializer(ModelSerializer):

    class Meta:
        model = DeliveryAddress
        exclude = ('id',)


class MyDeliveries_Items__ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ('name',)


class MyDeliveries_ItemsSerializer(ModelSerializer):
    product = MyDeliveries_Items__ProductSerializer()

    class Meta:
        model = OrderItem
        exclude = ('id',)
        depth = 1


class MyDeliveriesSerializer(ModelSerializer):

    items = MyDeliveries_ItemsSerializer(many=True)
    toaddress = MyDeliveries_ToaddressSerializer()

    class Meta:
        model = Order
        exclude = ('id', 'ordershipper', 'orderbycustomer')


class DeliveryServicerDetailSerializer(ModelSerializer):

    profile = DeliveryServicer__ProfileSerializer()
    mydeliveries = MyDeliveriesSerializer(many=True)

    class Meta:
        model = DeliveryServicer
        fields = "__all__"
        depth = 2


class DeliveryServicerUpdateSerializer(ModelSerializer):

    profile = DeliveryServicer__ProfileSerializer()

    class Meta:
        model = DeliveryServicer
        exclude = ('mydeliveries', )
        depth = 2


class DeliveryServicerRatingsUpdateSerializer(ModelSerializer):

    class Meta:
        model = DeliveryServicer
        fields = ('id', 'ratings')


# class DeliveryServicerDeliveryUpdateSerializer(ModelSerializer):

#     class Meta:
#         model = DeliveryServicer
#         fields = ('id', 'mydeliveries')


class DeliverServicerAvailableUpdateSerializer(ModelSerializer):

    class Meta:
        model = DeliveryServicer
        fields = ('id', 'available')


class Order__Customer__Profile_UserSerializer(ModelSerializer):
    # imported in other modules

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class Order__Customer__ProfileSerializer(ModelSerializer):

    user = Order__Customer__Profile_UserSerializer()

    class Meta:
        model = CustomerProfile
        exclude = ('id',)


class CheckOrderGiven__Order__CustomerSerializer(ModelSerializer):

    profile = Order__Customer__ProfileSerializer()

    class Meta:
        model = Customer
        fields = ('profile',)


class CheckOrderGiven__OrderSerializer(ModelSerializer):

    items = MyDeliveries_ItemsSerializer(many=True)
    toaddress = MyDeliveries_ToaddressSerializer()
    orderbycustomer = CheckOrderGiven__Order__CustomerSerializer()

    class Meta:
        model = Order
        exclude = ('ordershipper', )

# class CheckOrderGivenSerializer(ModelSerializer):

#     mydeliveries = CheckOrderGiven__OrderSerializer()

#     class Meta:
#         model = DeliveryServicer
#         fields = ('mydeliveries',)
