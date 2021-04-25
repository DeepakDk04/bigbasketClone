from django.urls import path

from .views import (

    CustomerCreateView,
    CustomerDetailView,
    CustomerUpdateView,

    CustomerProfileCreateView,
    CustomerProfileDetailView,
    UserUpdateView,
    CustomerProfileUpdateView,
    CustomerProfileDeleteView,

    AddressCreateView,
    AddressDetailView,
    AddressUpdateView,
    AddressDeleteView,

)


urlpatterns = [

    path('profil-create/', CustomerProfileCreateView.as_view()),
    path('profile-detail/<int:id>/', CustomerProfileDetailView.as_view()),
    
    path('user-update/<int:id>/', UserUpdateView.as_view()),
    path('profile-update/<int:id>/', CustomerProfileUpdateView.as_view()),
    # when calling profile-update, profile-user-update must called before if user property changed
    
    # path('profile-delete/<int:id>/', CustomerProfileDeleteView.as_view()),

    path('address-create/', AddressCreateView.as_view()),
    path('address-detail/<int:id>/', AddressDetailView.as_view()),
    path('address-update/<int:id>/', AddressUpdateView.as_view()),
    path('address-delete/<int:id>/', AddressDeleteView.as_view()),

    path('create/', CustomerCreateView.as_view()),
    path('detail/<int:id>/', CustomerDetailView.as_view()),
    path('update/<int:id>/', CustomerUpdateView.as_view()),

]
