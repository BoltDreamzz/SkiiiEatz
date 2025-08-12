from django.db import models
from django.utils.text import slugify
from accounts.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from core.utils import unique_slugify
# from restaurants.models import Restaurant
from supermarkets.models import Supermarket

# class Cart(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')
#     quantity = models.PositiveIntegerField(default=1)

# class Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     total = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed')])
#     created_at = models.DateTimeField(auto_now_add=True)


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.address}, {self.city}, {self.state}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Cart for {self.user.username} created at {self.created_at}"

class CartPack(models.Model):
    """
    Represents a 'pack' or a sub-cart inside the main Cart.
    For example: 'Pack 1', 'Pack 2', etc.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='packs')
    name = models.CharField(max_length=255, blank=True, null=True)  # Optional: "Lunch Pack", "Dinner Pack"
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    
    
    # Vendor-related (only one vendor per pack)
    # from restaurants.models import Restaurant
    restaurant = models.ForeignKey("restaurants.Restaurant", on_delete=models.CASCADE, null=True, blank=True)
    supermarket = models.ForeignKey(Supermarket, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name or f"Pack from {self.restaurant}"

class CartItem(models.Model):
    """
    Each item belongs to a specific pack in the cart.
    """
    pack = models.ForeignKey(CartPack, on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now=True,  null=True)
    
    def __str__(self):
        return f"{self.quantity} of {self.content_object} in Pack {self.pack.name or 'Unnamed'}"
    
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'), 
        ('completed', 'Completed')
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} for {self.user.username} - {self.status} - Total: {self.total}"

# core/models.py
class City(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name
