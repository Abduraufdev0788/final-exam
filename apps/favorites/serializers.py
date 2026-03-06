from rest_framework import serializers
from .models import Favorite
from apps.product.serializers import ProductViewSerializers


class FavoriteSerializer(serializers.ModelSerializer):
    product = ProductViewSerializers(read_only=True)

    class Meta:
        model = Favorite
        fields = ["id", "product", "created_at"]