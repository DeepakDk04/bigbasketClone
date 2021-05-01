from django.contrib import admin

from .models import JoinCode, ShopOwner
# Register your models here.

admin.site.register(ShopOwner)
admin.site.register(JoinCode)
