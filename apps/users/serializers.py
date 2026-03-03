from rest_framework import serializers
from .models import User
from apps.sellers.models import SellerProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'telegram_id', 'first_name', 'last_name', 'phone_number', 'role', 'avatar']


class UserUpdateSerializer(serializers.Serializer):
    username = serializers.CharField(required = False)
    first_name = serializers.CharField(required = False)
    last_name = serializers.CharField(required = False)
    phone_number = serializers.CharField(required = False)
    avatar = serializers.CharField(required = False)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save(update_fields=list(validated_data.keys()))
        return instance
    
class UpgradeToSellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerProfile
        fields = [
            "shop_name",
            "shop_description",
            "shop_logo",
            "region",
            "district"
        ]
    
    def validate(self, attrs):
        user = self.context['request'].user

        if user.role == 'seller':
            raise serializers.ValidationError("User is already a seller.")
        
        if hasattr(user, 'seller_profile'):
            raise serializers.ValidationError("User already has a seller profile.")
        
        return attrs
    
    def create(self, validated_data):
        user = self.context['request'].user
        seller_profile = SellerProfile.objects.create(user=user, **validated_data)
        user.role = User.Roles.SELLER
        user.save(update_fields=['role'])
        return seller_profile
    