from django.db import models

# from customer.models import Customer
from products.models import Product
from deliveryservice.models import DeliveryServicer

# Create your models here.


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.name + " [ " + str(self.quantity) + " ]"


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.name + " [ " + str(self.quantity) + " ]"


class Cart(models.Model):
    items = models.ManyToManyField("CartItem", default='empty')

    def __str__(self):

        cart = [item.product.name for item in self.items.all()]
        if self.items.count() != 0:
            return " , ".join(cart)
        else:
            return str(self.id) + " -empty"


class Order(models.Model):

    orderstatus = [

        ("notplaced", "notplaced"),
        ("placed", "placed"),
        ("delivery", "delivery"),
        ("reached", "reached"),
        ("cancelled", "cancelled"),

    ]

    items = models.ManyToManyField("OrderItem")
    orderbycustomer = models.ForeignKey(
        "customer.Customer", on_delete=models.CASCADE)
    ordershipper = models.ForeignKey(
        DeliveryServicer, on_delete=models.CASCADE)
    amount = models.IntegerField()
    status = models.CharField(
        max_length=10, choices=orderstatus, default="notplaced", blank=True, null=True)
    toaddress = models.ForeignKey(
        "customer.DeliveryAddress", on_delete=models.CASCADE, null=True)
    placedon = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id) + " ) " + self.orderbycustomer.profile.user.username
