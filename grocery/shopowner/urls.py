from django.urls import path

from .views import (

    GetJoinCodeAPIView,
    CancelJoinCodeAPIView,

    ShopOwnerSignUpAPIView,
    ShopOwnerDetailAPIView,
    ShopOwnerUpdateDetailAPIView,


    AddProductAPIView,
    UpdateProductAPIView,
    ProductDetailAdminAPIView,

    AddCategoryAPIView,
    UpdateCategoryAPIView,
    CategoryDetailAdminAPIView,

    AddOfferAPIView,
    UpdateOfferAPIView,
    OfferDetailAdminAPIView,

    StatisticAPIView,
    OrderDetailAdminAPIView,
    CustomerListAdminAPIView,
    DelivererListAdminAPIView,

)


urlpatterns = [

    path('get-joincode/', GetJoinCodeAPIView.as_view()),
    path('cancel-joincode/<str:code>/', CancelJoinCodeAPIView.as_view()),

    path('signup/', ShopOwnerSignUpAPIView.as_view()),
    path('detail/<int:id>/', ShopOwnerDetailAPIView.as_view()),
    path('update/<int:id>/', ShopOwnerUpdateDetailAPIView.as_view()),


    path('add-product/', AddProductAPIView.as_view()),
    path('update-product/<int:id>/', UpdateProductAPIView.as_view()),

    path('add-category/', AddCategoryAPIView.as_view()),
    path('update-category/<int:id>/', UpdateCategoryAPIView.as_view()),

    path('add-offer/', AddOfferAPIView.as_view()),
    path('update-offer/<int:id>/', UpdateOfferAPIView.as_view()),

    path('stat/', StatisticAPIView.as_view()),

    path('all-products/', ProductDetailAdminAPIView.as_view()),
    path('all-categories/', CategoryDetailAdminAPIView.as_view()),
    path('all-offers/', OfferDetailAdminAPIView.as_view()),
    path('all-orders/', OrderDetailAdminAPIView.as_view()),
    path('all-customers/', CustomerListAdminAPIView.as_view()),
    path('all-deliverers/', DelivererListAdminAPIView.as_view()),

]
