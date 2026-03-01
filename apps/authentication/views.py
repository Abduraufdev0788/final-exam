from apps.users.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from django.db import transaction
from .services import download_telegram_photo
from .serializers import RegisterSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import AllowAny


class RegisterApiView(APIView):    
    def post(self, request: Request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        telegram_id = serializer.validated_data["telegram_id"]
        username = serializer.validated_data.get("username", "")
        first_name = serializer.validated_data["first_name"]
        last_name = serializer.validated_data.get("last_name", "")
        phone_number = serializer.validated_data["phone_number"]
        avatar = serializer.validated_data.get("avatar")

        with transaction.atomic():
            user, created = User.objects.get_or_create(
                telegram_id=telegram_id,
                defaults={
                    "username": username,
                    "first_name": first_name,
                    "last_name": last_name,
                    "phone_number": phone_number,
                }
            )

            if avatar:
                avatar_file = download_telegram_photo(avatar)
                user.avatar.save(f"{telegram_id}.jpg", avatar_file)

            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "status": "success",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "user": {
                        "id": user.id,
                        "telegram_id": user.telegram_id,
                        "role": user.role,
                        "first_name": user.first_name,
                    }
                },
                status=status.HTTP_200_OK
            )
    
class CheckUserView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        telegram_id = request.query_params.get("telegram_id")

        if not telegram_id:
            return Response(
                {"error": "telegram_id required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        exists = User.objects.filter(telegram_id=telegram_id).exists()

        return Response(
            {"exists": exists},
            status=status.HTTP_200_OK
        )
class UserToken(APIView):
    def post(self, request):
        telegram_id = request.data.get("telegram_id")
        try:
            user = User.objects.get(telegram_id=telegram_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_200_OK
        )
