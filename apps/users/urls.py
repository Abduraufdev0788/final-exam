from django.urls import path
from .views import MeView, UpgradeToSeller

urlpatterns = [
    path("me/", MeView.as_view()),
    path("me/upgrade-to-seller/", UpgradeToSeller.as_view(), name="upgrade-to-seller")
]