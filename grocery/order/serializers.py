from rest_framework.serializers import ModelSerializer


from django.contrib.auth.models import User

from .models import Cart, CartItem, Order, OrderItem
from customer.models import DeliveryAddress
from deliveryservice.models import DeliveryServicer, DeliveryServicerProfile
from products.models import Product


class UserDisplaySerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class OrderResponseDisplay__OrderShipper__ProfileSerializer(ModelSerializer):
    user = UserDisplaySerializer()

    class Meta:
        model = DeliveryServicerProfile
        exclude = ('id',)


class OrderResponseDisplay__OrderShipperSerializer(ModelSerializer):

    profile = OrderResponseDisplay__OrderShipper__ProfileSerializer()

    class Meta:
        model = DeliveryServicer
        fields = ('ratings', 'profile')
        depth = 1


class OrderResponseDisplay__ToAddressSerializer(ModelSerializer):

    class Meta:
        model = DeliveryAddress
        exclude = ('id',)


class OrderResponseDisplaySerializer(ModelSerializer):

    ordershipper = OrderResponseDisplay__OrderShipperSerializer()
    toaddress = OrderResponseDisplay__ToAddressSerializer()

    class Meta:
        model = Order
        # fields = ('id', 'items', 'orderbycustomer',
        #           'ordershipper', 'amount', 'toaddress', 'status')
        exclude = ('id', 'items', 'orderbycustomer')
        depth = 1


class OrderCreateSerializer(ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'
        # fields = ('id', 'items', 'orderbycustomer',
        #           'ordershipper', 'amount', 'toaddress', 'status')


# {
# 	"items":[
# 		5,6
# 		],
#   "toaddress":13
# }


class CartItemSerializer(ModelSerializer):

    class Meta:
        model = CartItem
        fields = ("id", "product", "quantity")


###
class Cart__Items__ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ('name', 'image')


class Cart__ItemsSerializer(ModelSerializer):

    product = Cart__Items__ProductSerializer()

    class Meta:
        model = CartItem
        fields = "__all__"


class CartUpdateSerializer(ModelSerializer):

    items = Cart__ItemsSerializer(many=True)

    class Meta:
        model = Cart
        fields = "__all__"
        depth = 1

# {
#     "items":[
#         {
#             "product":1,
#             "quantity":1
#         },
#         {
#             "product":7,
#             "quantity":1
#         },
#     ]
# }


class OrderItemCreateSerializer(ModelSerializer):

    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderStatusUpdateSerializer(ModelSerializer):

    class Meta:
        model = Order
        fields = ('id', 'status')

# {
#     "status":"deliverd"
# }
