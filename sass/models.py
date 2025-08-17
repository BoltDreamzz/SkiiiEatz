from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
# from restaurants.models import Restaurant
# from pharmacy.models import Pharmacy
# from supermarkets.models import Supermarket
from accounts.models import User  # Assuming User model is in accounts app
# from core.models import Order
# User = get_user_model()


class Business(models.Model):
    BUSINESS_TYPES = (
        ('restaurant', 'Restaurant'),
        ('pharmacy', 'Pharmacy'),
        ('supermarket', 'Supermarket'),
    )
    business_type = models.CharField(max_length=50, choices=BUSINESS_TYPES)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='business_logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vendor.business_name} - {self.business_type}"

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vendor_profile')
    business_name = models.CharField(max_length=255)
    business_type = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True)

    phone = models.CharField(max_length=30, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    commission_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                            validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return f"{self.business_name} ({self.user.email})"

    def get_commission_percent(self):
        if self.commission_percent is not None:
            return float(self.commission_percent)
        try:
            return float(CommissionSetting.get_solo().percent)
        except Exception:
            return 10.0


# class Restaurant(models.Model):
#     business = models.OneToOneField(Business, on_delete=models.CASCADE, related_name='restaurant_details')
#     cuisine = models.CharField(max_length=200, blank=True, null=True)
#     opening_hours = models.TextField(blank=True, null=True)

# class Pharmacy(models.Model):
#     business = models.OneToOneField(Business, on_delete=models.CASCADE, related_name='pharmacy_details')
#     license_number = models.CharField(max_length=200, blank=True, null=True)

# class Supermarket(models.Model):
#     business = models.OneToOneField(Business, on_delete=models.CASCADE, related_name='supermarket_details')

class CommissionSetting(models.Model):
    percent = models.DecimalField(max_digits=5, decimal_places=2, default=10.00,
                                  validators=[MinValueValidator(0), MaxValueValidator(100)])
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def get_solo(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return f"Platform Commission: {self.percent}%"

class Earning(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='earnings')
    # order_id = models.CharField(max_length=128)
    order_id = models.ForeignKey('core.Order', on_delete=models.CASCADE, related_name='earnings')
    gross_amount = models.DecimalField(max_digits=12, decimal_places=2)
    commission_percent = models.DecimalField(max_digits=5, decimal_places=2)
    commission_amount = models.DecimalField(max_digits=12, decimal_places=2)
    net_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid_out = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.vendor} - {self.net_amount} (Order: {self.order_id})"

class PayoutRequest(models.Model):
    STATUS = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
        ('paid', 'Paid'),
    )
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='payout_requests')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    requested_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    admin_notes = models.TextField(blank=True, null=True)
    processed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.vendor.business_name} - {self.amount} - {self.status}"
