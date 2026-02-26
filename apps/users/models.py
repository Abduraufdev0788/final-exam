from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta

class User(AbstractUser):

    class Roles(models.TextChoices):
        CUSTOMER = 'CUSTOMER', 'Customer'
        SELLER = 'SELLER', 'Seller'
    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=14)
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.CUSTOMER)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)


    def __str__(self):
        return f"{self.first_name}   --- {self.telegram_id}  --- {self.role}"
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
 