from re import U
from django.db.models import fields
from .models import Customer, CustomerProfile, DeliveryAddress
from django.contrib.auth.models import User

from rest_framework.serializers import ModelSerializer


class ProfileCreateSerializer(ModelSerializer):

    class Meta:
        model = CustomerProfile
        fields = ['user', 'age', 'contactno']


class userViewOrUpdateSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'first_name', 'last_name']


class ProfileViewSerializer(ModelSerializer):

    user = userViewOrUpdateSerializer()

    class Meta:
        model = CustomerProfile
        fields = ['user', 'age', 'contactno']
        depth = 1


class ProfileUpdateSerializer(ModelSerializer):

    user = userViewOrUpdateSerializer()

    class Meta:
        model = CustomerProfile
        fields = ['user', 'age', 'contactno']

    def update(self, instance, validated_data):

        user = validated_data.get("user", {})

        username = user.get("username", False)
        if not username:
            username = instance.user.username

        email = user.get("email", False)
        if not email:
            email = instance.user.email

        first_name = user.get("first_name", False)
        if not first_name:
            first_name = instance.user.first_name

        last_name = user.get("last_name", False)
        if not last_name:
            last_name = instance.user.last_name

        instance.user.username = username
        instance.user.email = email
        instance.user.first_name = first_name
        instance.user.last_name = last_name

        instance.age = validated_data.get("age", instance.age)

        instance.contactno = validated_data.get(
            "contactno", instance.contactno)

        instance.save()

        return instance


class ProfileDeleteSerializer(ModelSerializer):

    class Meta:
        model = CustomerProfile
        fields = ['id']


class AddressCreateOrViewOrUpdateSerializer(ModelSerializer):

    class Meta:
        model = DeliveryAddress
        fields = ['doorno', 'street', 'area', 'landmark']


class CustomerCreateOrViewOrUpdateSerializer(ModelSerializer):

    class Meta:
        model = Customer
        fields = ['profile', 'address']


class CreateUserSerializer(ModelSerializer):
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
