from django.urls import path

from .views import ProductListView, ProductDetailView

urlpatterns = [
    path('all/', ProductListView.as_view()),
    path('detail/<int:id>/', ProductDetailView.as_view()),
]
