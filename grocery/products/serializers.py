from .models import Product
from rest_framework.serializers import ModelSerializer


class ProductListSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'offer', 'stockCount']



class ProductDetailSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'offer', 'stockCount']
        depth = 1
        