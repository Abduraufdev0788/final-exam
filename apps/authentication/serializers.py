from rest_framework import serializers
from apps.users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'telegram_id', 'first_name', 'last_name', 'phone_number', 'role', 'avatar']

class RegisterSerializer(serializers.Serializer):
    telegram_id = serializers.IntegerField(required=True)
    username = serializers.CharField(required=False, allow_blank=True, max_length=150)
    first_name = serializers.CharField(required=True, max_length=150)
    last_name = serializers.CharField(required=False, allow_blank=True)
    phone_number = serializers.CharField(required=True, max_length=14)
    avatar = serializers.CharField(required=False, allow_blank=True)

    def validate_telegram_id(self, value):
        if User.objects.filter(telegram_id=value).exists():
            raise serializers.ValidationError("Bu telegram_id bilan user mavjud")
        return value