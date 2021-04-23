from django.urls import path

from .views import RegisterAPIView, LoginAPIView
from knox.views import LogoutView, LogoutAllView


urlpatterns = [

    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('logoutall/', LogoutAllView.as_view()),

]
