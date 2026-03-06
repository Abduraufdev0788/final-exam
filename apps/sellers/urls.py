from django.urls import path
from .views import SellerProfileView, SellerProductsView

urlpatterns = [
    path("sellers/<int:pk>/", SellerProfileView.as_view(), name="seller-profile"),
    path("sellers/<int:pk>/products", SellerProductsView.as_view(), name="seller-products"),

]
