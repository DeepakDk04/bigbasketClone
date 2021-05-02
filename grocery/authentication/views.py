from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from django.contrib.auth import login
from django.contrib.auth.models import Group, User

from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView

from .serializers import UserSerializer, RegisterSerializer

# Create your views here.

# Register API


class RegisterAPIView(GenericAPIView):
    '''
    Creates the user account in customer group (default)
    '''
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        group = Group.objects.get(name='Customer')
        user.groups.add(group)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


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
