from order.models import Order
from rest_framework.serializers import ModelSerializer


from .models import Customer, CustomerProfile, DeliveryAddress
from django.contrib.auth.models import User


class ProfileCreateSerializer(ModelSerializer):

    class Meta:
        model = CustomerProfile
        fields = ['id', 'user', 'age', 'gender', 'contactno']


class userModelCustomSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'first_name', 'last_name']


class ProfileViewSerializer(ModelSerializer):

    user = userModelCustomSerializer()

    class Meta:
        model = CustomerProfile
        fields = ['id', 'user', 'age', 'gender', 'contactno']
        depth = 1


class ProfileUpdateSerializer(ModelSerializer):

    user = userModelCustomSerializer()

    class Meta:
        model = CustomerProfile
        fields = ['id', 'user', 'age', 'gender', 'contactno']
        read_only_fields = ('user',)


class ProfileDeleteSerializer(ModelSerializer):

    class Meta:
        model = CustomerProfile
        fields = ['id']


class AddressCreateOrViewOrUpdateSerializer(ModelSerializer):

    class Meta:
        model = DeliveryAddress
        fields = ['id', 'doorno', 'street', 'area', 'landmark']


class AddressDeleteSerializer(ModelSerializer):

    class Meta:
        model = DeliveryAddress
        fields = ['id']


class CustomerCreateOrUpdateSerializer(ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id', 'profile', 'address', 'cart', 'myorders']


class CustomerView__ProfileSerializer(ModelSerializer):

    user = userModelCustomSerializer()

    class Meta:
        model = CustomerProfile
        fields = '__all__'


# class CustomerView__MyOrdersSerializer(ModelSerializer):

#     class Meta:
#         model = Order
#         fields = ['id', ]


class CustomerViewSerializer(ModelSerializer):

    profile = CustomerView__ProfileSerializer()
    # myorders = CustomerView__MyOrdersSerializer()

    class Meta:
        model = Customer
        fields = ['id', 'profile', 'address', 'cart', 'myorders']
        depth = 2


class CustomerDeleteSerializer(ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id']
