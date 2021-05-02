from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class ShopOwner(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()

    def __str__(self) -> str:
        return self.user.username


class JoinCode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    createdby = models.ForeignKey(
        'ShopOwner', on_delete=models.SET_NULL, null=True, related_name="createdby")
    timestamp = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)
    joiner = models.ForeignKey(
        'ShopOwner', on_delete=models.SET_NULL, blank=True, null=True, related_name="joiner")

    def __str__(self) -> str:
        return self.code
