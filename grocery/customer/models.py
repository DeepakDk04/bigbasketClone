from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    profile = models.OneToOneField('CustomerProfile', on_delete=models.CASCADE)
    address = models.OneToOneField(
        'DeliveryAddress', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.profile.user.username


class CustomerProfile(models.Model):
    # user => username, email, password, first_name, last_name, is_active, last_login, date_joined, is_admin, is_superuser, is_staff
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    contactno = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username


class DeliveryAddress(models.Model):
    doorno = models.CharField(max_length=10)
    street = models.CharField(max_length=50)
    area = models.CharField(max_length=50)
    landmark = models.CharField(max_length=50)

    def __str__(self):
        return self.street + " in " + self.area
