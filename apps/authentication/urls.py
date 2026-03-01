from django.urls import path
from .views import RegisterApiView, CheckUserView, UserToken
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("check-user/", CheckUserView.as_view()),
    path("telegram-login/", RegisterApiView.as_view()),
    path("token/", UserToken.as_view()),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
]