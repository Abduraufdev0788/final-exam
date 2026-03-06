from datetime import timedelta, timezone

from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, UpdateAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from .models import Product
from .serializers import ProductViewSerializers, ProductCreateSerializer, ProductDetailSerializer
from .filters import ProductFilter
from django.db.models import F



class ProductView(ListCreateAPIView):
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

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductCreateSerializer
        return ProductViewSerializers

    def perform_create(self, serializer):
        user = self.request.user

        if user.role != "seller":
            raise PermissionDenied("Faqat sotuvchi mahsulot qo‘sha oladi.")

        serializer.save(
            seller=user,
            status="moderatsiyada"
        )

class ProductDetailView(RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        product = get_object_or_404(
            Product.objects.select_related("seller")
            .prefetch_related("images"),
            pk=self.kwargs["pk"],
            status="aktiv"
        )

        Product.objects.filter(pk=product.pk).update(
            view_count=F("view_count") + 1
        )

        product.refresh_from_db()

        return product
    


class ProductUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        if product.seller != request.user:
            return Response({"error": "Ruxsat yo'q"}, status=403)

        serializer = ProductViewSerializers(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if product.status == "aktiv":
            serializer.save(status="moderatsiyada")
        else:
            serializer.save()

        return Response(serializer.data)


    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        if product.seller != request.user:
            return Response({"error": "Ruxsat yo'q"}, status=403)

        product.delete()

        return Response({"message": "Product o'chirildi"})
    
class ActivSellerView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        if product.seller != request.user:
            return Response({"error": "Ruxsat yo'q"}, status=403)

        product.status = "aktiv"
        product.save()

        return Response({"message": "Product aktiv qilindi"})
    
class ProductArchiveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        if product.seller != request.user:
            return Response({"error": "Ruxsat yo'q"}, status=403)

        product.status = "arxivlangan"
        product.save(update_fields=["status"])

        return Response({"message": "Product arxivlandi"})
    

class ProductSoldView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        if product.seller != request.user:
            return Response({"error": "Ruxsat yo'q"}, status=403)

        product.status = "sotilgan"
        product.save(update_fields=["status"])

        return Response({"message": "Product sotilgan"})
    

