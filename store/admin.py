from django.contrib import admin
from .models import Item, OrderItem, Order, Category, ShippingAddress, Size


admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(ShippingAddress)
admin.site.register(Size)
