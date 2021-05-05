from django.urls import path, include

from .views import (

    RegisterAPIView,
    LoginAPIView,
    ChangePasswordView

)
from knox.views import LogoutView, LogoutAllView


urlpatterns = [

    path('register/', RegisterAPIView.as_view()),

    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('logoutall/', LogoutAllView.as_view()),

    path('change-password/', ChangePasswordView.as_view()),
    path('forgot-password/', include('django_rest_passwordreset.urls',
                                     namespace='password_reset')),


]


# (POST) forgot-password/reset_password/
#           - request a reset password token by using the email parameter


# (POST) forgot-password/reset_password/confirm/
#           - using a valid token, the users password is set to the provided password
# {
#     "token":"3339e80fe05e5ca9fc74799213f81a093d1f",
#     "password":"Password@123"
# }


# (POST) forgot-password/reset_password/validate_token/
#            - will return a 200 if a given token is valid


'''
urlpatterns = [
    url(r'^validate_token/', reset_password_validate_token, name="reset-password-validate"),
    url(r'^confirm/', reset_password_confirm, name="reset-password-confirm"),
    url(r'^', reset_password_request_token, name="reset-password-request"),
]
'''
