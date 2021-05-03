from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from .models import Product
from .serializers import ProductListSerializer, ProductDetailSerializer


from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
# Create your views here.


class ProductListView(ListAPIView):
    '''
    Displays all the Products
    '''
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]

    pagination_class = PageNumberPagination

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'category__name']
    ordering_fields = ['stockCount', 'price']

    ordering = ['-stockCount']


class ProductDetailView(RetrieveAPIView):
    '''
    Displays Single Product with Full Details
    '''
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'
