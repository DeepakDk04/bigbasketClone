from django.db import models
from django.db.models import fields
from .models import Customer, CustomerProfile, DeliveryAddress
from django.contrib.auth.models import User

from rest_framework.serializers import ModelSerializer


class ProfileCreateSerializer(ModelSerializer):

    class Meta:
        model = CustomerProfile
        fields = ['id', 'user', 'age', 'contactno']


class userModelCustomSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'first_name', 'last_name']


class ProfileViewSerializer(ModelSerializer):

    user = userModelCustomSerializer()

    class Meta:
        model = CustomerProfile
        fields = ['id', 'user', 'age', 'contactno']
        depth = 1


class ProfileUpdateSerializer(ModelSerializer):

    user = userModelCustomSerializer()

    class Meta:
        model = CustomerProfile
        fields = ['id', 'user', 'age', 'contactno']
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
        fields = ['id', 'profile', 'address']


class CustomerView__ProfileSerializer(ModelSerializer):

    user = userModelCustomSerializer()

    class Meta:
        model = CustomerProfile
        fields = '__all__'


class CustomerViewSerializer(ModelSerializer):

    profile = CustomerView__ProfileSerializer()

    class Meta:
        model = Customer
        fields = ['id', 'profile', 'address']
        depth = 2


class CustomerDeleteSerializer(ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id']


class CreateUserSerializer(ModelSerializer):
    '''
    used in signUP
    '''
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
