from shopowner.models import ShopOwner
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser

# Create your views here.


class OwnerAccountSignUpAPIView(CreateAPIView):

    queryset = ShopOwner.objects.all()
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
