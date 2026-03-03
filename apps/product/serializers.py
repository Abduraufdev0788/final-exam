from rest_framework import serializers
from .models import Product

class ProductViewSerializers(serializers.ModelSerializer):
    seller_name = serializers.CharField(source= "seller.first_name", read_only = True)
    class Meta:
        model = Product
        fields= ["title",
            "price",
            "price_type",
            "region",
            "view_count",
            "seller_name",
            "created_at"
            ]
