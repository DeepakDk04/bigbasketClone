from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=50)
    category = models.ManyToManyField('Category')
    offer = models.ForeignKey(
        'Offer', on_delete=models.CASCADE, blank=True, null=True)
    price = models.IntegerField(default=0)
    stockCount = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.name


class Offer(models.Model):
    description = models.CharField(max_length=100)
    percentage = models.IntegerField()
    start = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField()

    def __str__(self):
        return self.description
