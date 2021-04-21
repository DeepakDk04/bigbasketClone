from .models import Product
from rest_framework import serializers


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name', 'category', 'isOffer', 'offer', 'stockCount']
        depth = 1


