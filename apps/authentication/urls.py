from django.urls import path
from .views import RegisterApiView, CheckUserView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("telegram-login/", RegisterApiView.as_view()),
    path("check-user/", CheckUserView.as_view()),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
]