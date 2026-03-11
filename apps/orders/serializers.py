from rest_framework import serializers
from .models import Order
from apps.product.models import Product


class OrderSerializer(serializers.ModelSerializer):

    product_title = serializers.CharField(source="product.title", read_only=True)
    buyer_username = serializers.CharField(source="buyer.username", read_only=True)
    seller_username = serializers.CharField(source="seller.username", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "product",
            "product_title",
            "buyer",
            "buyer_username",
            "seller",
            "seller_username",
            "final_price",
            "status",
            "meeting_location",
            "meeting_time",
            "notes",
            "created_at",
        ]
        read_only_fields = [
            "buyer",
            "seller",
            "final_price",
            "status",
            "created_at",
        ]