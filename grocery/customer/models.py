from django.db import models

from order.models import Cart
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    '''
    Customer Account
    '''
    profile = models.OneToOneField(
        'CustomerProfile', on_delete=models.CASCADE, default='')
    address = models.ManyToManyField('DeliveryAddress',  blank=True)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    myorders = models.ManyToManyField('order.Order', blank=True)

    def __str__(self):
        return self.profile.user.username


class CustomerProfile(models.Model):
    '''
    Customer Profile Details
    '''
    genderchoices = [
        ("Male", "Male"), ("Female", "Female"), ("Others", "Others")
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    gender = models.CharField(max_length=6, choices=genderchoices)
    contactno = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username + ' , ' + str(self.age)


class DeliveryAddress(models.Model):
    '''
    Address details of customer for product delivery
    '''
    doorno = models.CharField(max_length=10)
    street = models.CharField(max_length=50)
    area = models.CharField(max_length=50)
    landmark = models.CharField(max_length=50)

    def __str__(self):
        return self.street + " , " + self.area
