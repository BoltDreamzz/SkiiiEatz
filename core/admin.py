from django.contrib import admin
from .models import City, Order, Cart, CartItem
from restaurants.models import Restaurant, MenuItemCategory, Meal, MenuItem


# Register your models here.
admin.site.register(City)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Restaurant)
admin.site.register(MenuItemCategory)
# admin.site.register(Meal)
admin.site.register(MenuItem)