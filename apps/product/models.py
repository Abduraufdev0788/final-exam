from django.db import models
from django.conf import settings
from apps.category.models import Category


class Product(models.Model):

    class Condition(models.TextChoices):
        NEW = "yangi", "Yangi"
        IDEAL = "ideal", "Ideal"
        GOOD = "yaxshi", "Yaxshi"
        FAIR = "qoniqarli", "Qoniqarli"

    class PriceType(models.TextChoices):
        FIXED = "qat'iy", "Qat'iy"
        NEGOTIABLE = "kelishiladi", "Kelishiladi"
        FREE = "bepul", "Bepul"
        EXCHANGE = "ayirboshlash", "Ayirboshlash"

    class Status(models.TextChoices):
        MODERATION = "moderatsiyada", "Moderatsiyada"
        ACTIVE = "aktiv", "Aktiv"
        REJECTED = "rad_etilgan", "Rad etilgan"
        SOLD = "sotilgan", "Sotilgan"
        ARCHIVED = "arxivlangan", "Arxivlangan"

    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="products"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    title = models.CharField(max_length=200)
    description = models.TextField()

    condition = models.CharField(
        max_length=20,
        choices=Condition.choices
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    price_type = models.CharField(
        max_length=20,
        choices=PriceType.choices
    )

    region = models.CharField(max_length=100)
    district = models.CharField(max_length=100)

    view_count = models.PositiveIntegerField(default=0)
    favorite_count = models.PositiveIntegerField(default=0)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.MODERATION
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    published_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title
    


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(upload_to="products/")
    order = models.PositiveIntegerField(default=0)
    is_main = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.title} image"