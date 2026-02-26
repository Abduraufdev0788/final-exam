from apps.users.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from django.db import transaction
from .services import download_telegram_photo


class RegisterApiView(APIView):
    def get(self, request:Request):
        data = request.query_params.get("telegram_id")
    
        if not data:
            return Response({"status":"error"})
        
        user = User.objects.filter(telegram_id=data).first()

        if user:
            return Response({"status":"exists"})
        
        return Response({"status":False})
    
    def post(self, request: Request):

        telegram_id = request.data.get("telegram_id")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        phone_number = request.data.get("phone")
        avatar_file_id = request.data.get("avatar")

        if not telegram_id or not first_name or not phone_number:
            return Response(
                {"status": "error", "message": "Majburiy maydonlar yetishmayapti"},
                status=400
            )

        if User.objects.filter(telegram_id=telegram_id).exists():
            return Response(
                {"status": "exists"},
                status=200
            )

        with transaction.atomic():
            user = User.objects.create(
                telegram_id=telegram_id,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
            )

     
            if avatar_file_id:
                avatar_file = download_telegram_photo(avatar_file_id)
                user.avatar.save(f"{telegram_id}.jpg", avatar_file)

        return Response(
            {"status": "success"},
            status=201
        )

