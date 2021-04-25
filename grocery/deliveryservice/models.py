from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class DeliveryServicer(models.Model):
    rating = [("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")]
    profile = models.OneToOneField(
        'DeliveryServicerProfile', on_delete=models.CASCADE, default='')
    ratings = models.CharField(max_length=1, choices=rating)

    def __str__(self):
        return self.profile.user.username


class DeliveryServicerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    contactno = models.CharField(max_length=10)
    # ordersTaken = models.ManyToManyField("Order", null=True)

    def __str__(self):
        return self.user.username
