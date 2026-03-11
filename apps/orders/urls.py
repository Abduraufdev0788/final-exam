from django.urls import path
from .views import OrderViews, OrderDetailView

urlpatterns = [
    path("orders/", OrderViews.as_view(), name="orders"),
    path("orders/<int:pk>/", OrderDetailView.as_view()),
]