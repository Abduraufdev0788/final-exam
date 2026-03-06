from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from .models import Category
from .serializers import CategorySerializer
from apps.product.serializers import ProductViewSerializers
from rest_framework.filters  import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from apps.product.filters import ProductFilter
from django.shortcuts import get_object_or_404
from apps.product.models import Product

class CategoryListView(ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Category.objects.filter(
            parent__isnull=True,
            is_active=True
        ).order_by("order_num")
    

class CategoryDetailView(RetrieveAPIView):
    queryset = Category.objects.prefetch_related("children")
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"


class CategoryProductsView(ListAPIView):
    serializer_class = ProductViewSerializers
    permission_classes = [AllowAny]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_class = ProductFilter
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "price", "view_count"]
    ordering = ["-created_at"]

    def get_queryset(self):
        slug = self.kwargs["slug"]

        category = get_object_or_404(Category, slug=slug)

        category_ids = [category.id]
        category_ids += list(
            category.category_set.values_list("id", flat=True)
        )

        return Product.objects.select_related(
            "seller", "category"
        ).filter(
            category_id__in=category_ids,
            status="aktiv"
        )