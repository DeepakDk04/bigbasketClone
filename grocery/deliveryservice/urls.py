from django.urls import path

from customer.views import UserUpdateView

from .views import (

    DeliverServicerSignUpAPIView,

    DeliverServicerProfileCreateView,
    # DeliverServicerProfileDetailView,
    DeliverServicerProfileUpdateView,

    DeliverServicerCreateView,
    DeliverServicerDetailView,
    DeliverServicerRatingsUpdateView,
    DeliverServicerDeliveryUpdateView,
    DeliverServicerAvailableUpdateView,

)

urlpatterns = [

    path('user-create/', DeliverServicerSignUpAPIView.as_view()),
    path('servicer-profile/create/', DeliverServicerProfileCreateView.as_view()),
    path('servicer/create/', DeliverServicerCreateView.as_view()),

    # path('servicer-profile/detail/<int:id>/',
    #      DeliverServicerProfileDetailView.as_view()),
    path('servicer/detail/<int:id>/', DeliverServicerDetailView.as_view()),

    path('user-update/<int:id>/', UserUpdateView.as_view()),
    path('servicer-profile/update/<int:id>/',
         DeliverServicerProfileUpdateView.as_view()),

    path('servicer/update-ratings/<int:id>/',
         DeliverServicerRatingsUpdateView.as_view()),
    path('servicer/update-delivery/<int:id>/',
         DeliverServicerDeliveryUpdateView.as_view()),
    path('servicer/update-available/<int:id>/',
         DeliverServicerAvailableUpdateView.as_view()),


]
