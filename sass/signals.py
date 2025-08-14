from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Earning
from core.models import Order  # adjust to your actual order model

@receiver(post_save, sender=Order)
def create_earning_on_order_completion(sender, instance, created, **kwargs):
    if not created and instance.status == 'completed':
        vendor = getattr(instance, 'vendor', None)
        if not vendor and hasattr(instance, 'business'):
            vendor = instance.business.vendor
        if not vendor:
            return
        gross = Decimal(instance.total_amount)
        commission_percent = Decimal(vendor.get_commission_percent())
        commission_amount = (gross * commission_percent) / Decimal(100)
        net = gross - commission_amount
        if not Earning.objects.filter(order_id=instance.pk).exists():
            Earning.objects.create(
                vendor=vendor,
                order_id=str(instance.pk),
                gross_amount=gross,
                commission_percent=commission_percent,
                commission_amount=commission_amount,
                net_amount=net,
            )
