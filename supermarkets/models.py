# supermarkets/models.py
from django.db import models
# from django.utils.text import slugify
from core.utils import unique_slugify
from django.utils import timezone
from datetime import timedelta, time
from geopy.geocoders import Nominatim
from django.utils.text import slugify
from core.utils import unique_slugify
from sass.models import Business

# 💰 Budget Categories
CATEGORIES_CHOICES = [
    ('$', 'Budget'),
    ('$$', 'Mid-range'),
    ('$$$', 'Premium'),
    ('$$$$', 'Luxury'),
]

class Supermarket(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    address = models.TextField()
    owner = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='supermarkets/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    

    city = models.ForeignKey('core.City', on_delete=models.CASCADE)
    
    is_open = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    # 🛍️ Enhanced fields
    is_sponsored = models.BooleanField(default=False)
    tag = models.CharField(max_length=100, blank=True, null=True)  # E.g. "10% Off", "Free Delivery"
    tags = models.CharField(max_length=255, blank=True, null=True)  # Comma-separated if needed

    budget_category = models.CharField(max_length=10, choices=CATEGORIES_CHOICES, default='$')

    open_time = models.TimeField(default=time(8, 0))   # Default 8:00 AM
    close_time = models.TimeField(default=time(22, 0)) # Default 10:00 PM
    preparation_time = models.PositiveIntegerField(default=30)  # Optional: Picking/packing time in minutes
    business = models.OneToOneField(Business, on_delete=models.CASCADE, related_name='supermarket_details', null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def is_open_now(self):
        now = timezone.localtime().time()
        return self.open_time <= now < self.close_time

    def time_until_open(self):
        now = timezone.localtime()
        open_today = now.replace(
            hour=self.open_time.hour,
            minute=self.open_time.minute,
            second=0,
            microsecond=0
        )

        if now.time() < self.open_time:
            return open_today - now
        else:
            return (open_today + timedelta(days=1)) - now

    def open_countdown_parts(self):
        delta = self.time_until_open()
        total_seconds = int(delta.total_seconds())
        days = total_seconds // 86400
        hours = (total_seconds % 86400) // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return {
            "days": days,
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds,
        }

    def status_text(self):
        if self.is_open_now():
            return "Open Now"
        return f"Closed – Opens at {self.open_time.strftime('%I:%M %p')}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)

        # Geocode
        if not self.latitude or not self.longitude:
            geolocator = Nominatim(user_agent="my_supermarket_app")
            full_address = f"{self.address}, {self.city.name}"
            location = geolocator.geocode(full_address)
            if location:
                self.latitude = location.latitude
                self.longitude = location.longitude

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SupermarketProductCategory(models.Model):
    name = models.CharField(max_length=100)
    supermarket = models.ForeignKey(Supermarket, on_delete=models.CASCADE, related_name='product_categories')

    def __str__(self):
        return f"{self.name} ({self.supermarket.name})"


class SupermarketProduct(models.Model):
    supermarket = models.ForeignKey(Supermarket, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(SupermarketProductCategory, on_delete=models.SET_NULL, null=True, blank=True)
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=8, decimal_places=2)

    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)

    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    tag = models.CharField(max_length=100, blank=True, null=True)  # E.g. "Bestseller", "Organic", etc.
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.supermarket.name})"
