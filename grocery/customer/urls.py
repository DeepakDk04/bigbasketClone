from django.urls import path

from .views import (

    CustomerProfileCreateView,
    CustomerProfileDetailView,
    CustomerProfileUpdateView,
    CustomerProfileDeleteView,

)


urlpatterns = [
    path('create/', CustomerProfileCreateView.as_view()),
    path('detail/<int:id>/', CustomerProfileDetailView.as_view()),
    path('update/<int:id>/', CustomerProfileUpdateView.as_view()),
    path('delete/<int:id>/', CustomerProfileDeleteView.as_view()),

]
