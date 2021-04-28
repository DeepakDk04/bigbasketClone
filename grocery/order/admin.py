from order.models import Cart, CartItem, Order, OrderItem
from django.contrib import admin

# Register your models here.

admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
