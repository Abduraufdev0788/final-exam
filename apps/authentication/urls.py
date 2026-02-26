from django.urls import path
from .views import RegisterApiView

urlpatterns = [
    path("telegram-login/", RegisterApiView.as_view())
    
]