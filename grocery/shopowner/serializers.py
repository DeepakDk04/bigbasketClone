from products.models import Category, Offer, Product
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


class ShopOwnerUpdateDetailSerializer(ModelSerializer):

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


class AddProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"


class AddCategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class AddOfferSerializer(ModelSerializer):

    class Meta:
        model = Offer
        fields = "__all__"


class UpdateProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"


class UpdateCategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class UpdateOfferSerializer(ModelSerializer):

    class Meta:
        model = Offer
        fields = "__all__"


class ProductAdminViewSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"
        depth = 1


class CategoryAdminViewSerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class OfferAdminViewSerializer(ModelSerializer):

    class Meta:
        model = Offer
        fields = "__all__"
