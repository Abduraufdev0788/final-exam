import requests
from django.core.files.base import ContentFile
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.settings import TELEGRAM_BOT_TOKEN

class TelegramFileDownloadError(Exception):
    """Telegram file yuklab olishda xatolik"""
    pass

def download_telegram_photo(file_id: str) -> ContentFile:

    if not file_id:
        raise TelegramFileDownloadError("file_id bo'sh")

    try:
        response = requests.get(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getFile",
            params={"file_id": file_id},
            timeout=5
        )
        response.raise_for_status()
        file_info = response.json()

    except requests.RequestException as e:
        raise TelegramFileDownloadError(f"Telegram API bilan bog‘lanib bo‘lmadi: {str(e)}")

    # 🔹 2️⃣ Telegram javobini tekshiramiz
    if not file_info.get("ok"):
        raise TelegramFileDownloadError(
            f"Telegram xatolik qaytardi: {file_info}"
        )

    file_path = file_info["result"]["file_path"]

    # 🔹 3️⃣ Rasmni yuklab olish
    try:
        file_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}"
        file_response = requests.get(file_url, timeout=5)
        file_response.raise_for_status()

    except requests.RequestException as e:
        raise TelegramFileDownloadError(f"Rasmni yuklab bo‘lmadi: {str(e)}")

    return ContentFile(
        file_response.content,
        name=f"{file_id}.jpg"
    )




class URLSafeJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is not None:
            return super().authenticate(request)

        raw_token = request.query_params.get('token')
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token