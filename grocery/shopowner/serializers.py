from .models import JoinCode, ShopOwner
from rest_framework.serializers import ModelSerializer


class ShopOwnerCreateSerializer(ModelSerializer):

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