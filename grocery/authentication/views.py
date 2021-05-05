from rest_framework.generics import GenericAPIView, UpdateAPIView


from rest_framework.permissions import AllowAny, IsAuthenticated


from django.contrib.auth.models import User, Group
from knox.models import AuthToken


from rest_framework.authtoken.serializers import AuthTokenSerializer
from .serializers import (

    UserSerializer,
    RegisterSerializer,
    ChangePasswordSerializer

)


from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView


from rest_framework.response import Response
from rest_framework import status


# Create your views here.


class RegisterAPIView(GenericAPIView):
    '''
    Creates the user account in customer group (default)
    '''
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        group = Group.objects.get(name='Customer')
        user.groups.add(group)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        }, status=status.HTTP_201_CREATED)


class LoginAPIView(KnoxLoginView):
    '''
    Login to the User Account
    '''
    permission_classes = (AllowAny,)

    def get_post_response_data(self, request, token, instance):
        # UserSerializer = self.get_user_serializer_class()
        UsersSerializer = UserSerializer

        data = {
            'expiry': self.format_expiry_datetime(instance.expiry),
            'token': token
        }
        if UsersSerializer is not None:
            data["user"] = UsersSerializer(
                request.user,
                context=self.get_context()
            ).data

        if request.user.groups.filter(name="Customer").exists():
            usertype = 'Customer'
            account_id = request.user.customerprofile.customer.id

        elif request.user.groups.filter(name="Deliveryservicer").exists():
            usertype = 'Deliverservicer'
            account_id = request.user.deliveryservicerprofile.deliveryservicer.id

        elif request.user.groups.filter(name="Shopowner").exists():
            usertype = 'Shopowner'
            account_id = request.user.shopowner.id

        else:
            usertype = 'unknown'
            account_id = 0

        extra_data = {
            'usertype': usertype,
            'account_id': account_id,
        }

        data.update(extra_data)

        return data

    def post(self, request, format=None):

        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        login(request, user)

        return super(LoginAPIView, self).post(request, format=None)


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """

    model = User
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):

        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                errorMessage = {"old_password": ["Wrong password."]}
                return Response(errorMessage, status=status.HTTP_400_BAD_REQUEST)

            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()

            successMessage = {'message': 'Password updated successfully'}
            return Response(successMessage, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
