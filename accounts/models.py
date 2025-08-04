from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    is_vendor = models.BooleanField(default=False)
    is_delivery_agent = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email
    
    
# models.py
import os
import random
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

# User = get_user_model()

def get_avatar_upload_path(instance, filename):
    return os.path.join('avatars', filename)

class Avatar(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=get_avatar_upload_path)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ForeignKey(Avatar, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username
