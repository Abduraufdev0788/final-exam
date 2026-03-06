from rest_framework import serializers
from .models import Product, ProductImage

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


class ProductCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            "category",
            "title",
            "description",
            "condition",
            "price",
            "price_type",
            "region",
            "district",
        ]
    
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "order", "is_main"]


class ProductDetailSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(
        source="seller.first_name",
        read_only=True
    )
    seller_id = serializers.IntegerField(
        source="seller.id",
        read_only=True
    )
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "description",
            "price",
            "price_type",
            "condition",
            "region",
            "district",
            "view_count",
            "favorite_count",
            "seller_id",
            "seller_name",
            "images",
            "created_at",
        ]


class ProductUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            "category",
            "title",
            "description",
            "condition",
            "price",
            "price_type",
            "region",
            "district",
        ]