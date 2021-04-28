from django.db import models
from rest_framework import fields
from rest_framework.serializers import ModelSerializer

from .models import Cart, CartItem, Order


class OrderCreateSerializer(ModelSerializer):

    class Meta:
        model = Order
        fields = ('id', 'items', 'orderbycustomer',
                  'ordershipper', 'amount', 'toaddress', 'status')

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


class CartUpdateSerializer(ModelSerializer):

    # items = CartItemSerializer()

    class Meta:
        model = Cart
        fields = ["id", "items"]
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


class OrderStatusUpdateSerializer(ModelSerializer):

    class Meta:
        model = Order
        fields = ('id', 'status')

# {
#     "status":"deliverd"
# }
