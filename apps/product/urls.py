from django.urls import path
from .views import ProductView, ProductDetailView, ProductArchiveView, ActivSellerView, ProductSoldView

urlpatterns = [
    path("products/", ProductView.as_view(), name = 'products'),
    path("products/<int:pk>/", ProductDetailView.as_view()),
    path("products/<int:pk>/archive/", ProductArchiveView.as_view()),
    path("products/<int:pk>/active/", ActivSellerView.as_view()),
    path("products/<int:pk>/sold/", ProductSoldView.as_view()),
]