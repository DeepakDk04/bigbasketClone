from .models import Product
from rest_framework.serializers import ModelSerializer


class ProductListSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductDetailSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"
        depth = 1
