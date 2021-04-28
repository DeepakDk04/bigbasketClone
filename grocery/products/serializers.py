from .models import Product
from rest_framework.serializers import ModelSerializer


class ProductListSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'offer', 'stockCount', 'price')


class ProductDetailSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'offer', 'stockCount', 'price')
        depth = 1
