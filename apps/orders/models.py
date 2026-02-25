from django.db import models
from apps.product.models import Product
from django.conf import settings

class Order(models.Model):

    class Status(models.TextChoices):
        Kutilyapti = "kutilyapti", "Kutilyapti"
        Kelishilgan = "kelishilgan", "Kelishilgan"
        Sotib_olingan = "sotib olingan", "Sotib olingan"
        Bekor_qilingan = "bekor qilingan", "Bekor qilingan"
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sales")
    final_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.Kutilyapti)
    meeting_location = models.CharField(blank=True)
    meeting_time = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.product.title} ({self.status})"

