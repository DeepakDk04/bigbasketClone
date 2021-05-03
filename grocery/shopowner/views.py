from rest_framework.response import Response
from shopowner.models import ShopOwner
from rest_framework.generics import DestroyAPIView, ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from django.contrib.auth.models import User, Group

from authentication.serializers import RegisterSerializer, UserSerializer
from knox.models import AuthToken

from .models import JoinCode
from products.models import Product, Offer, Category

from .permissions import IsOwnerGroup, IsOwnerDetail, IsOwnerJoinCode
from rest_framework import status

from .serializers import (

    ShopOwnerCreateSerializer,
    JoinCodeCreateSerializer,
    JoinCodeDetailSerializer,
    ShopOwnerDetailSerializer,

    userModelCustomSerializer,
    ShopOwnerUpdateDetailSerializer,

    AddProductSerializer,
    AddCategorySerializer,
    AddOfferSerializer,

    UpdateProductSerializer,
    UpdateCategorySerializer,
    UpdateOfferSerializer,

    ProductAdminViewSerializer,
    CategoryAdminViewSerializer,
    OfferAdminViewSerializer,

)

# Create your views here.


class ShopOwnerSignUpAPIView(GenericAPIView):
    '''
    Creates the user account in admin group using the joincode
    '''
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def _isJoinCodeValid(self, joincode):
        ''' Check if the joincode is valid  '''
        if JoinCode.objects.filter(code=joincode).exists():
            JoinerCode = JoinCode.objects.get(code=joincode)
            if not JoinerCode.used:
                return True
        return False

    def _addJoinerInJoinCodeInstance(self, joincode, joiner):
        ''' The joiner will be saved with the joincode instance   '''
        JoinCodeInstance = JoinCode.objects.get(code=joincode)

        JoinCodeInstance.joiner = joiner
        JoinCodeInstance.used = True
        JoinCodeInstance.save()

        # send_notification(JoinCodeInstance.createdby, joiner, message="1 new user joined using your code")

    def post(self, request, *args, **kwargs):
        '''  Overrided method for nested writes  '''
        joincode = request.data.get("joincode", False)

        if not joincode:
            errorMessage = {"field_error": {
                "joincode": "joincode is required"}}
            return Response(data=errorMessage, status=status.HTTP_400_BAD_REQUEST)

        if not self._isJoinCodeValid(joincode):
            errorMessage = {"value_error": {
                "joincode": "joincode is not valid"}}
            return Response(data=errorMessage, status=status.HTTP_401_UNAUTHORIZED)

        request.data.pop("joincode")

        age = request.data.get("age", False)

        if not age:
            errorMessage = {
                "field_error": {"age": "age is required"}
            }
            return Response(data=errorMessage, status=status.HTTP_400_BAD_REQUEST)

        request.data.pop("age")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.is_staff = True
        user.save()

        group = Group.objects.get(name='Shopowner')
        user.groups.add(group)

        shopowner_data = {"user": user.id, "age": age}

        shopowner_serializer = ShopOwnerCreateSerializer(data=shopowner_data)
        shopowner_serializer.is_valid(raise_exception=True)

        new_shopowner_account = shopowner_serializer.save()

        self._addJoinerInJoinCodeInstance(joincode, new_shopowner_account)

        ownerDetail = ShopOwnerDetailSerializer(new_shopowner_account).data

        return Response({
            # "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "detail": ownerDetail,
            "token": AuthToken.objects.create(user)[1]
        })


class GetJoinCodeAPIView(RetrieveAPIView):
    ''' Get the joincode, To join in a admin group  '''
    queryset = JoinCode.objects.all()
    serializer_class = JoinCodeCreateSerializer
    permission_classes = (IsAuthenticated, IsOwnerGroup,)

    def _generateUniqueJoinCode(self):
        '''  Get unique code '''
        import random
        import string

        s = ''

        letterCount = random.randint(3, 5)
        numberCount = random.randint(3, 5)
        suffleCount = random.randint(1, 10)

        for _ in range(letterCount):
            s += str(random.choice(string.ascii_letters))

        for _ in range(numberCount):
            s += str(random.choice(string.digits))

        lt = list(s)

        for i in range(suffleCount):
            random.shuffle(lt)

        newCode = "".join(lt)

        if JoinCode.objects.filter(code=newCode).exists():
            return self._generateUniqueJoinCode()

        return newCode

    def get(self, request, *args, **kwargs):
        ''' 
        didn't allow to generate newcode ,if a joincode is generated already
        Returns existing joincode for the requested admin,
        if all codes were used for joining, generated and return new code
        '''
        shopowner = request.user.shopowner

        unUsedJoinCode = JoinCode.objects.filter(
            createdby=shopowner).filter(used=False)

        if unUsedJoinCode.exists():
            ''' get instance from the queryset '''
            instance = unUsedJoinCode.first()
            joinCodeDetail = JoinCodeDetailSerializer(instance).data
            return Response(joinCodeDetail, status=status.HTTP_200_OK)

        joinCodeData = {
            "code": self._generateUniqueJoinCode(),
            "createdby": shopowner.id
        }

        joinCodeSerializer = self.get_serializer(data=joinCodeData)
        joinCodeSerializer.is_valid(raise_exception=True)
        newJoinCode = joinCodeSerializer.save()

        joinCodeDetail = JoinCodeDetailSerializer(newJoinCode).data

        return Response(joinCodeDetail, status=status.HTTP_200_OK)


class CancelJoinCodeAPIView(DestroyAPIView):
    ''' Invalidate the Existing Joincode, no can can join using it later '''
    queryset = JoinCode.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerJoinCode, )
    lookup_field = 'code'

    def delete(self, request, *args, **kwargs):

        JoinCodeInstance = self.get_object()

        if JoinCodeInstance.used:
            joiner = ShopOwnerDetailSerializer(JoinCodeInstance.joiner).data
            message = {"detail": {
                "already joined with the code": joiner}}
            return Response(data=message, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().delete(request, *args, **kwargs)


class ShopOwnerDetailAPIView(RetrieveAPIView):
    '''
    Get Detail of Shopowner Account
    '''
    queryset = ShopOwner.objects.all()
    serializer_class = ShopOwnerDetailSerializer
    permission_classes = (IsAuthenticated, IsOwnerDetail, )
    lookup_field = 'id'


class ShopOwnerUpdateDetailAPIView(UpdateAPIView):
    '''
    Get Detail of Shopowner Account
    '''
    queryset = ShopOwner.objects.all()
    serializer_class = ShopOwnerUpdateDetailSerializer
    permission_classes = (IsAuthenticated, IsOwnerDetail, )
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        ''' nested updates for user instance and account instance  '''
        shopowner_instance = self.get_object()
        user_data = request.data.get("user", False)
        account_data = request.data.get("account", False)

        if user_data:
            ''' Updates the user instance '''
            user_instance = shopowner_instance.user
            user_updateserializer = userModelCustomSerializer(
                user_instance, data=user_data, partial=True)
            user_updateserializer.is_valid(raise_exception=True)
            user_updateserializer.save()

        if account_data:
            ''' Updates the shopowner instance '''
            shopowner_update_serializer = self.get_serializer(
                shopowner_instance, data=account_data, partial=True)
            shopowner_update_serializer.is_valid(raise_exception=True)
            shopowner_update_serializer.save()

        updatedShopOwnerData = ShopOwnerDetailSerializer(
            shopowner_instance).data

        return Response(data=updatedShopOwnerData, status=status.HTTP_202_ACCEPTED)


class AddProductAPIView(CreateAPIView):
    ''' Add New Products to the database  '''
    queryset = Product.objects.all()
    serializer_class = AddProductSerializer
    permission_classes = (IsAuthenticated, IsOwnerGroup, )


class AddCategoryAPIView(CreateAPIView):
    ''' Add new Category to the database '''
    queryset = Category.objects.all()
    serializer_class = AddCategorySerializer
    permission_classes = (IsAuthenticated, IsOwnerGroup, )


class AddOfferAPIView(CreateAPIView):
    ''' Add new Offer to the database '''
    queryset = Offer.objects.all()
    serializer_class = AddOfferSerializer
    permission_classes = (IsAuthenticated, IsOwnerGroup, )


class UpdateProductAPIView(UpdateAPIView):
    ''' Update New Products to the database  '''
    queryset = Product.objects.all()
    serializer_class = UpdateProductSerializer
    permission_classes = (IsAuthenticated, IsOwnerGroup, )
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        product_instance = self.get_object()

        product_serializer = self.get_serializer(
            product_instance, data=request.data, partial=True)
        product_serializer.is_valid(raise_exception=True)

        product_serializer.save()

        productData = ProductAdminViewSerializer(product_instance).data
        return Response(data=productData, status=status.HTTP_200_OK)


class UpdateCategoryAPIView(UpdateAPIView):
    ''' Update new Category to the database '''
    queryset = Category.objects.all()
    serializer_class = UpdateCategorySerializer
    permission_classes = (IsAuthenticated, IsOwnerGroup, )
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        category_instance = self.get_object()

        category_serializer = self.get_serializer(
            category_instance, data=request.data, partial=True)
        category_serializer.is_valid(raise_exception=True)

        category_serializer.save()

        categoryData = CategoryAdminViewSerializer(category_instance).data
        return Response(data=categoryData, status=status.HTTP_200_OK)


class UpdateOfferAPIView(UpdateAPIView):
    ''' Update new Offer to the database '''
    queryset = Offer.objects.all()
    serializer_class = UpdateOfferSerializer
    permission_classes = (IsAuthenticated, IsOwnerGroup, )
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        offer_instance = self.get_object()

        offer_serializer = self.get_serializer(
            offer_instance, data=request.data, partial=True)
        offer_serializer.is_valid(raise_exception=True)

        offer_serializer.save()

        OfferData = OfferAdminViewSerializer(offer_instance).data
        return Response(data=OfferData, status=status.HTTP_200_OK)


class DashBoardView(GenericAPIView):
    ''' Get details for the dashboard '''
    permission_classes = (IsAuthenticated, IsOwnerGroup, IsAdminUser)

    def get(self, request, *args, **kwargs):

        allProducts = Product.objects.all()
        allCategories = Category.objects.all()
        allOffers = Offer.objects.all()

        productData = ProductAdminViewSerializer(allProducts, many=True).data
        categoryData = CategoryAdminViewSerializer(
            allCategories, many=True).data
        OfferData = OfferAdminViewSerializer(allOffers, many=True).data

        allData = {
            "products": productData,
            "categories": categoryData,
            "offers": OfferData
        }

        return Response(data=allData, status=status.HTTP_200_OK)
