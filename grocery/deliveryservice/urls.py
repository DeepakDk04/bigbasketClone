from django.urls import path

from customer.views import UserUpdateView

from .views import (

    DeliverServicerProfileCreateView,
    DeliverServicerProfileDetailView,
    DeliverServicerProfileUpdateView,

    DeliverServicerCreateView,
    DeliverServicerDetailView,
    DeliverServicerUpdateView,

)

urlpatterns = [

    path('servicer-profile/create/', DeliverServicerProfileCreateView.as_view()),
    path('servicer-profile/detail/<int:id>/',
         DeliverServicerProfileDetailView.as_view()),
    path('user-update/<int:id>/', UserUpdateView.as_view()),
    path('servicer-profile/update/<int:id>/',
         DeliverServicerProfileUpdateView.as_view()),

    path('servicer/create/', DeliverServicerCreateView.as_view()),
    path('servicer/detail/<int:id>/', DeliverServicerDetailView.as_view()),
    path('servicer/update/<int:id>/', DeliverServicerUpdateView.as_view()),

]
