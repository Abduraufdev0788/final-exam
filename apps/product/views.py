from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductViewSerializers
from .filters import ProductFilter

class ProductView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductViewSerializers

    queryset = Product.objects.select_related(
        "seller", "category"
    ).filter(status="aktiv")

    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter
    ]

    filterset_class = ProductFilter
    search_fields = ["title", "description"]
    ordering_fields = ['created_at', 'view_count', 'price']
    ordering = ['-created_at']

    

