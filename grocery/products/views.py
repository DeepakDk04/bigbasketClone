from django.shortcuts import render

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from .models import Product
from .serializers import ProductListSerializer, ProductDetailSerializer

# Create your views here.


class ProductListView(ListAPIView):
    '''
    Displays all the Products
    '''
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]


class ProductDetailView(RetrieveAPIView):
    '''
    Displays Single Product with Full Details
    '''
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'
