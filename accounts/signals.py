from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile, Avatar, User
from django.contrib.auth import get_user_model
import random

# User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        avatars = Avatar.objects.all()
        avatar = random.choice(avatars) if avatars.exists() else None
        UserProfile.objects.create(user=instance, avatar=avatar)
