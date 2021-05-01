from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class ShopOwner(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()


class JoinCode(models.Model):
    code = models.CharField(max_length=10, unique=True)
