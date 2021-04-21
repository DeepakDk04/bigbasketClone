from django.urls import path

from .views import sampleView

urlpatterns = [
    path('products/', sampleView, name='pro'),
]
