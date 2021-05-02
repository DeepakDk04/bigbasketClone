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

class JoinCodeCreateSerializer(ModelSerializer):

    class Meta:
        model = JoinCode
        fields = ('createdby', 'code')

class JoinCodeDetailSerializer(ModelSerializer):

    class Meta:
        model = JoinCode
        fields = ('code',)