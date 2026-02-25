from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    class Roles(models.TextChoices):
        CUSTOMER = 'CUSTOMER', 'Customer'
        SELLER = 'SELLER', 'Seller'
    telegram_id = models.BigIntegerField(unique=True)
    username = models.CharField(unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    phone_number = models.CharField(max_length=13)
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.CUSTOMER)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.first_name}   --- {self.telegram_id}  --- {self.role}"
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
 