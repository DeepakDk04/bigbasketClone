from django.urls import path

from . import views

urlpatterns = [
    path('all/', views.ProductListView.as_view() ),
    path('detail/<int:id>/', views.ProductDetailView.as_view() ),
]
