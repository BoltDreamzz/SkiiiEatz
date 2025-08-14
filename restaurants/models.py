# restaurants/models.py
from django.db import models
from django.utils.text import slugify
from core.utils import unique_slugify
from core.models import City

from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.contenttypes.fields import GenericForeignKey
from geopy.geocoders import Nominatim
from datetime import time
from sass.models import Business

from django.utils.text import slugify

# Choices dictionary for restaurant categories eg $$, $$$, etc.
CATEGORIES_CHOICES = [
    ('$ Affordable', 'Budget'),
    ('$$ Pricy', 'Mid-range'),
    ('$$$ Quite Pricy ', 'Premium'),
    ('$$$$ Expensive', 'Luxury'),
]

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    address = models.TextField()
    owner = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='restaurants/')
    created_at = models.DateTimeField(auto_now_add=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    is_open = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    is_sponsored = models.BooleanField(default=False)
    tag = models.CharField(max_length=100, blank=True, null=True) # EG Free Delivery, 10% Off, etc.
    preparation_time = models.PositiveIntegerField(default=30)  # in minutes
    
    # Add tags but not comma separated
    tags = models.CharField(max_length=255, blank=True, null=True)  # Comma-separated tags
    # Add categories choice field eg $$ $$$ etc
    budget_category = models.CharField(max_length=50, choices=CATEGORIES_CHOICES, default='$ Affordable') 
    # Open and close 
    open_time = models.TimeField(default=time(8, 0))   # default 8:00 AM
    close_time = models.TimeField(default=time(22, 0)) # default 10:00 PM   
    business = models.OneToOneField(Business, on_delete=models.CASCADE, related_name='restaurant_details', null=True, blank=True)
    


    def is_open_now(self):
        now = timezone.localtime().time()
        return self.open_time <= now < self.close_time

    def time_until_open(self):
        """Return timedelta until next opening (assumes open/close same day)"""
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
        """Break down timedelta into days, hours, minutes, seconds"""
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
            self.slug = slugify(self.name)

        # Geocode if no lat/lng provided
        if not self.latitude or not self.longitude:
            geolocator = Nominatim(user_agent="my_restaurant_app")
            full_address = f"{self.address}, {self.city.name}"
            location = geolocator.geocode(full_address)

            if location:
                self.latitude = location.latitude
                self.longitude = location.longitude

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

class Meal(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='meals/')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    available = models.BooleanField(default=True)
    
    
# restaurants/models.py

class MenuItemCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_categories', null=True, blank=False)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    item_category = models.ForeignKey(MenuItemCategory, on_delete=models.CASCADE, related_name='menu_items', null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='menu_items/')
    available = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=1.2)
    tag = models.CharField(max_length=100, default='Healthy', blank=True, null=True)  # EG Free Delivery, 10% Off, etc.
    date_posted = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} ({self.restaurant.name})"
