from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class DeliveryServicer(models.Model):
    '''
    Delivery Servicer Account
    '''
    rating = [(0, 0), (1, 1), (2, 2),
              (3, 3), (4, 4), (5, 5)]

    profile = models.OneToOneField(
        'DeliveryServicerProfile', on_delete=models.CASCADE, default='')
    ratings = models.IntegerField(
        choices=rating, default=0, blank=True, null=True)
    mydeliveries = models.ManyToManyField(
        "order.Order", blank=True, default='0')

    available = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.profile.user.username


class DeliveryServicerProfile(models.Model):
    '''
    Delivery Servicer Profile
    '''
    genderchoices = [
        ("Male", "Male"), ("Female", "Female"), ("Others", "Others")
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    gender = models.CharField(max_length=6, choices=genderchoices)
    contactno = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username + ' , age ' + str(self.age)
