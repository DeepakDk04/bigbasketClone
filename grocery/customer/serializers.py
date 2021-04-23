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

    # def update(self, instance, validated_data):

    #     user = validated_data.get("user", {})

    #     # serializer = userModelCustomSerializer(
    #     #     instance.user, data=user, partial=True)

    #     # serializer.is_valid(raise_exception=True)

    #     # user = serializer.save()

    #     username = user.get("username", False)
    #     if not username:
    #         username = instance.user.username

    #     email = user.get("email", False)
    #     if not email:
    #         email = instance.user.email

    #     first_name = user.get("first_name", False)
    #     if not first_name:
    #         first_name = instance.user.first_name

    #     last_name = user.get("last_name", False)
    #     if not last_name:
    #         last_name = instance.user.last_name

    #     instance.user.username = username
    #     instance.user.email = email
    #     instance.user.first_name = first_name
    #     instance.user.last_name = last_name
    #     # instance.user = user

    #     instance.age = validated_data.get("age", instance.age)

    #     instance.contactno = validated_data.get(
    #         "contactno", instance.contactno)

    #     instance.save()

    #     return instance


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
