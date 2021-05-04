from customer.models import Customer, CustomerProfile, DeliveryAddress
from deliveryservice.models import DeliveryServicer, DeliveryServicerProfile
from order.models import Order, OrderItem
from products.models import Category, Offer, Product
from django.contrib.auth.models import User
from .models import JoinCode, ShopOwner
from rest_framework.serializers import ModelSerializer


class ShopOwnerCreateSerializer(ModelSerializer):

    class Meta:
        model = ShopOwner
        fields = "__all__"


class userModelCustomSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ShopOwnerDetailSerializer(ModelSerializer):

    user = userModelCustomSerializer()

    class Meta:
        model = ShopOwner
        fields = "__all__"
        depth = 1


class ShopOwnerUpdateDetailSerializer(ModelSerializer):

    class Meta:
        model = ShopOwner
        fields = "__all__"


class JoinCodeCreateSerializer(ModelSerializer):

    class Meta:
        model = JoinCode
        fields = ('createdby', 'code')


class JoinCodeDetailSerializer(ModelSerializer):

    class Meta:
        model = JoinCode
        fields = ('code',)


class AddProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"


class AddCategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class AddOfferSerializer(ModelSerializer):

    class Meta:
        model = Offer
        fields = "__all__"


class UpdateProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"


class UpdateCategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class UpdateOfferSerializer(ModelSerializer):

    class Meta:
        model = Offer
        fields = "__all__"


class ProductAdminViewSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"
        depth = 1


class CategoryAdminViewSerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class OfferAdminViewSerializer(ModelSerializer):

    class Meta:
        model = Offer
        fields = "__all__"


class items_productSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name')


class Order_itemsSerializer(ModelSerializer):
    product = items_productSerializer()

    class Meta:
        model = OrderItem
        fields = "__all__"
        depth = 1


class user_UsernameSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('username',)


class Shipper_profileSerializer(ModelSerializer):
    user = user_UsernameSerializer()

    class Meta:
        model = DeliveryServicerProfile
        fields = ('user',)


class Order_shipperSerializer(ModelSerializer):
    profile = Shipper_profileSerializer()

    class Meta:
        model = DeliveryServicer
        fields = ('id', 'profile')
        depth = 2


class Order_toaddressSerializer(ModelSerializer):
    class Meta:
        model = DeliveryAddress
        exclude = ('id', )


class Customer_ProfileSerializer(ModelSerializer):
    user = user_UsernameSerializer()

    class Meta:
        model = CustomerProfile
        fields = ('user',)


class Order_CustomerSerializer(ModelSerializer):
    profile = Customer_ProfileSerializer()

    class Meta:
        model = Customer
        fields = ('id', 'profile')
        depth = 2


class OrderAdminViewSerializer(ModelSerializer):
    items = Order_itemsSerializer(many=True)
    orderbycustomer = Order_CustomerSerializer()
    ordershipper = Order_shipperSerializer()
    toaddress = Order_toaddressSerializer()

    class Meta:
        model = Order
        fields = "__all__"
        depth = 1
        # fields = ('id', 'items', 'orderbycustomer',
        #           'ordershipper', 'amount', 'toaddress', 'status')


class user_fullDetailSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'last_login', 'date_joined')


class Customer_ProfileSerializer(ModelSerializer):
    user = user_fullDetailSerializer()

    class Meta:
        model = CustomerProfile
        exclude = ('id',)
        depth = 1


class CustomerAdminViewSerializer(ModelSerializer):
    profile = Customer_ProfileSerializer()

    class Meta:
        model = Customer
        fields = ('id', 'profile', 'address')
        depth = 1


class Deliverer_ProfileSerializer(ModelSerializer):

    user = user_fullDetailSerializer()

    class Meta:
        model = DeliveryServicerProfile
        fields = "__all__"
        depth = 1


class DelivererAdminViewSerializer(ModelSerializer):
    profile = Deliverer_ProfileSerializer()

    class Meta:
        model = DeliveryServicer
        exclude = ('mydeliveries',)
        depth = 1
