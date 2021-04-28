from .views import OrderCreateAPTView, UpdateCartAPIView, OrderStatusUpdateAPIView
from django.urls import path


urlpatterns = [
    path('create/', OrderCreateAPTView.as_view()),
    path('cart-update/<int:id>/', UpdateCartAPIView.as_view()),
    path('status-update/<int:id>/', OrderStatusUpdateAPIView.as_view()),
]
