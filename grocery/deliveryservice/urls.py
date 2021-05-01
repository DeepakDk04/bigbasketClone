from django.urls import path

from customer.views import UserUpdateView

from .views import (

    DeliverServicerSignUpAPIView,


    DeliverServicerCreateView,
    DeliverServicerDetailView,
    DeliverServicerUpdateView,
    DeliverServicerRatingsUpdateView,
    
    DeliverServicerAvailableUpdateView,
    CheckOrderGiven,

)

urlpatterns = [

    path('user-create/', DeliverServicerSignUpAPIView.as_view()),
    path('servicer/create/', DeliverServicerCreateView.as_view()),

    path('servicer/detail/<int:id>/', DeliverServicerDetailView.as_view()),

    path('user-update/<int:id>/', UserUpdateView.as_view()),


    path('servicer/update-ratings/<int:id>/',
         DeliverServicerRatingsUpdateView.as_view()),

    path('servicer/update-available/<int:id>/',
         DeliverServicerAvailableUpdateView.as_view()),

    path('servicer/update/<int:id>/', DeliverServicerUpdateView.as_view()),
    path('servicer/check-order-given/<int:id>/', CheckOrderGiven.as_view()),

]
