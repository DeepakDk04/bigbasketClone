from deliveryservice.models import DeliveryServicer, DeliveryServicerProfile
from rest_framework.serializers import ModelSerializer


from django.contrib.auth.models import User
from products.models import Product
from order.models import Cart, CartItem, Order, OrderItem
from .models import Customer, CustomerProfile, DeliveryAddress


class ProfileCreateSerializer(ModelSerializer):

    class Meta:
        model = CustomerProfile
        fields = ['id', 'user', 'age', 'gender', 'contactno']


class userModelCustomSerializer(ModelSerializer):
    # imported in other modules

    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'first_name', 'last_name']


# class ProfileViewSerializer(ModelSerializer):

#     user = userModelCustomSerializer()

#     class Meta:
#         model = CustomerProfile
#         fields = ['id', 'user', 'age', 'gender', 'contactno']
#         depth = 1


class ProfileUpdateSerializer(ModelSerializer):

    user = userModelCustomSerializer()

    class Meta:
        model = CustomerProfile
        fields = ['id', 'user', 'age', 'gender', 'contactno']
        # read_only_fields = ('user',)


# class ProfileDeleteSerializer(ModelSerializer):

#     class Meta:
#         model = CustomerProfile
#         fields = ['id']


class AddressCreateOrViewOrUpdateSerializer(ModelSerializer):

    class Meta:
        model = DeliveryAddress
        fields = ['id', 'doorno', 'street', 'area', 'landmark']


# class AddressDeleteSerializer(ModelSerializer):

#     class Meta:
#         model = DeliveryAddress
#         fields = ['id']


class CustomerCreateOrUpdateSerializer(ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id', 'profile', 'address', 'cart', 'myorders']


# class CustomerUpdateCustom__UserSerializer(ModelSerializer):

#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'first_name', 'last_name']


class CustomerView__ProfileSerializer(ModelSerializer):

    user = userModelCustomSerializer()

    class Meta:
        model = CustomerProfile
        fields = '__all__'


class CustomerView__MyOrders__Items__ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ('name',)


class CustomerView__MyOrders__ItemsSerializer(ModelSerializer):

    product = CustomerView__MyOrders__Items__ProductSerializer()

    class Meta:
        model = OrderItem
        exclude = ('id',)


class CustomerView__MyOrdersSerializer(ModelSerializer):

    items = CustomerView__MyOrders__ItemsSerializer(many=True)

    class Meta:
        model = Order
        exclude = ('id', 'orderbycustomer', 'toaddress')


class CustomerView__Cart__Items__ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ('name',)


class CustomerView__Cart__ItemsSerializer(ModelSerializer):

    product = CustomerView__Cart__Items__ProductSerializer()

    class Meta:
        model = CartItem
        fields = "__all__"


class CustomerView__CartSerializer(ModelSerializer):

    items = CustomerView__Cart__ItemsSerializer(many=True)

    class Meta:
        model = Cart
        fields = "__all__"
        depth = 1


class CustomerViewSerializer(ModelSerializer):

    profile = CustomerView__ProfileSerializer()
    myorders = CustomerView__MyOrdersSerializer(many=True)
    cart = CustomerView__CartSerializer()

    class Meta:
        model = Customer
        fields = ['id', 'profile', 'address', 'cart', 'myorders']
        depth = 2


class CustomerUpdateCustomSerializer(ModelSerializer):

    profile = CustomerView__ProfileSerializer()

    class Meta:
        model = Customer
        fields = ['id', 'profile', 'address']
        depth = 2


class CustomerDeleteSerializer(ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id']


class OrderShipper__Profile__UserSerializer(ModelSerializer):
    # imported in other modules
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class OrderShipper__ProfileSerializer(ModelSerializer):

    user = OrderShipper__Profile__UserSerializer()

    class Meta:
        model = DeliveryServicerProfile
        exclude = ('id',)
        depth = 1


class CustomerPlacedOrders__OrderShipperSerializer(ModelSerializer):

    profile = OrderShipper__ProfileSerializer()

    class Meta:
        model = DeliveryServicer
        fields = ('profile', )


class CustomerPlacedOrders__ToAddressSerializer(ModelSerializer):

    class Meta:
        model = DeliveryAddress
        exclude = ('id',)


class CustomerPlacedOrdersSerializer(ModelSerializer):

    items = CustomerView__MyOrders__ItemsSerializer(many=True)
    ordershipper = CustomerPlacedOrders__OrderShipperSerializer()
    toaddress = CustomerPlacedOrders__ToAddressSerializer()

    class Meta:
        model = Order
        exclude = ('id', 'orderbycustomer')
        depth = 2
