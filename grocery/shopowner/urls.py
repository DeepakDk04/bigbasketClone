from django.urls import path

from .views import (

    ShopOwnerSignUpAPIView,
    GetJoinCodeAPIView,
    CancelJoinCodeAPIView,
    ShopOwnerDetailAPIView,
    ShopOwnerUpdateDetailAPIView,
    AddProductAPIView,
    AddCategoryAPIView,
    AddOfferAPIView,
    UpdateProductAPIView,
    UpdateCategoryAPIView,
    UpdateOfferAPIView,
    DashBoardView,

)


urlpatterns = [

    path('signup/', ShopOwnerSignUpAPIView.as_view()),
    path('detail/<int:id>/', ShopOwnerDetailAPIView.as_view()),
    path('update/<int:id>/', ShopOwnerUpdateDetailAPIView.as_view()),

    path('get-joincode/', GetJoinCodeAPIView.as_view()),
    path('cancel-joincode/<str:code>/', CancelJoinCodeAPIView.as_view()),

    path('add-product/', AddProductAPIView.as_view()),
    path('update-product/<int:id>/', UpdateProductAPIView.as_view()),

    path('add-category/', AddCategoryAPIView.as_view()),
    path('update-category/<int:id>/', UpdateCategoryAPIView.as_view()),

    path('add-offer/', AddOfferAPIView.as_view()),
    path('update-offer/<int:id>/', UpdateOfferAPIView.as_view()),

    path('dashboard/', DashBoardView.as_view()),

]
