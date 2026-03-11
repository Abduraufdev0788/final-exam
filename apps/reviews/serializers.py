from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    reviewer_username = serializers.CharField(source="reviewer.username", read_only=True)
    seller_username = serializers.CharField(source="seller.username", read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "order",
            "reviewer",
            "reviewer_username",
            "seller",
            "seller_username",
            "rating",
            "comment",
            "created_at",
        ]
        read_only_fields = ["reviewer", "seller", "created_at"]