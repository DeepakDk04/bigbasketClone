from rest_framework.response import Response
from shopowner.models import ShopOwner
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAdminUser

from django.contrib.auth.models import User, Group

from authentication.serializers import RegisterSerializer, UserSerializer
from knox.models import AuthToken

from .models import JoinCode

from .permissions import IsOwnerGroup, IsOwnerDetail
from rest_framework import status

from .serializers import (

    ShopOwnerCreateSerializer,
    JoinCodeCreateSerializer,
    JoinCodeDetailSerializer,
    ShopOwnerDetailSerializer,

)

# Create your views here.


class ShopOwnerSignUpAPIView(GenericAPIView):
    '''
    Creates the user account in admin group using the joincode
    '''
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def _isJoinCodeValid(self, joincode):

        if JoinCode.objects.filter(code=joincode).exists():
            JoinerCode = JoinCode.objects.get(code=joincode)
            if not JoinerCode.used:
                return True
        return False

    def _addJoinerInJoinCodeInstance(self, joincode, joiner):

        JoinCodeInstance = JoinCode.objects.get(code=joincode)

        JoinCodeInstance.joiner = joiner
        JoinCodeInstance.used = True
        JoinCodeInstance.save()

        # send_notification(JoinCodeInstance.createdby, joiner, message="1 new user joined using your code")

    def post(self, request, *args, **kwargs):

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

    queryset = JoinCode.objects.all()
    serializer_class = JoinCodeCreateSerializer
    permission_classes = (IsOwnerGroup,)

    def _generateUniqueJoinCode(self):
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

        shopowner = request.user.shopowner

        unUsedJoinCode = JoinCode.objects.filter(
            createdby=shopowner).filter(used=False)

        if unUsedJoinCode.exists():

            joinCodeDetail = JoinCodeDetailSerializer(unUsedJoinCode).data
            return Response(joinCodeDetail, status=status.status.HTTP_200_OK)

        joinCodeData = {
            "joincode": self._generateUniqueJoinCode(),
            "createdby": shopowner.id
        }

        joinCodeSerializer = self.get_serializer(data=joinCodeData)
        joinCodeSerializer.is_valid(raise_exception=True)
        newJoinCode = joinCodeSerializer.save()

        joinCodeDetail = JoinCodeDetailSerializer(newJoinCode).data

        return Response(joinCodeDetail, status=status.status.HTTP_200_OK)


class ShopOwnerDetailAPIView(RetrieveAPIView):

    queryset = ShopOwner.objects.all()
    serializer_class = ShopOwnerDetailSerializer()
    permission_classes = (IsOwnerDetail, )
