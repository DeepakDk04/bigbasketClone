from django.urls import path

from .views import (
    
    ShopOwnerSignUpAPIView,
    GetJoinCodeAPIView,
    
    )

urlpatterns = [

    path('signup/', ShopOwnerSignUpAPIView.as_view()),
    path('get-joincode/', GetJoinCodeAPIView.as_view()),

]
