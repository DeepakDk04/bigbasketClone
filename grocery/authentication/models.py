from django.db import models

# Create your models here.

from django.dispatch import receiver
from django.urls import reverse
from django.core.mail import send_mail


from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    # _link = reverse('password_reset:reset-password-request')
    _link = 'http://localhost:8000/auth/forgot-password/confirm/'
    # forget password link chage it after frontend works
    tokenKey = reset_password_token.key
    email_plaintext_message = "You are requested to reset the BigbasketAcccount Password \nCopy and paste this link on a new tab :\n\n {}?token={} \n\nIgnore if you are not requested...".format(
        _link, tokenKey)

    send_mail(
        # title:
        subject="Password Reset for {title}".format(
            title="The BigBasket Merchendice"),
        # message:
        message=email_plaintext_message,
        # from:
        from_email=None,  # "noreply@somehost.local", use the Default_Email_ID in settings
        # to:
        recipient_list=[reset_password_token.user.email]
    )
