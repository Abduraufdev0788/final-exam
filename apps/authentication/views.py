from .redis_client import redis_client
from apps.users.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from django.db import transaction
from .services import download_telegram_photo
from .serializers import RegisterSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
import random
import json
from .redis_client import redis_client


class RegisterApiView(APIView):
    permission_classes = [AllowAny]
    def get(self, request: Request):
        telegram_id = request.query_params.get("telegram_id")

        if not telegram_id:
            return Response(
                {"error": "telegram_id required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.filter(telegram_id=telegram_id).first()

        if not user:
            return Response(
                {"status": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        code = str(random.randint(100000, 999999))
        
        redis_client.setex(
            f"login_code:{code}",
            120,
            telegram_id
        )

        serializer = UserSerializer(user)

        return Response({"code": code, "user": serializer.data, "status": "success"}, status=status.HTTP_200_OK)    
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
            user = User.objects.create(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number
            )

            if avatar:
                avatar_file = download_telegram_photo(avatar)
                user.avatar.save(f"{telegram_id}.jpg", avatar_file)

            code = str(random.randint(100000, 999999))

            redis_client.setex(
                f"otp_{telegram_id}",
                120,
                code
            )
        return Response(
            {"code": code},
            status=status.HTTP_200_OK
        )
    

class CheckUserView(APIView):
        permission_classes = [AllowAny]

        def post(self, request:Request)->Response:
            code = request.data.get("code")

            if not code or len(code) != 6 or not code.isdigit():
                return Response(
                    {"error": "Kod noto‘g‘ri"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 2️⃣ Redisdan telegram_id olish
            telegram_id = redis_client.get(f"login_code:{code}")

            if not telegram_id:
                return Response(
                    {"error": "Kod xato yoki muddati o‘tgan"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 3️⃣ Userni topish
            user = User.objects.filter(telegram_id=telegram_id).first()
            print(user)

            if not user:
                return Response(
                    {"error": "User topilmadi"},
                    status=status.HTTP_404_NOT_FOUND
                )

            redis_client.delete(f"login_code:{code}")

            refresh = RefreshToken.for_user(user)

            return Response({
                "status": "success",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        
class UserLogOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request)->Response:
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"status": "success log out"}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)