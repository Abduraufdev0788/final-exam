from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import Request
from django.shortcuts import get_object_or_404
from .models import SellerProfile
from .serializers import SellerProfileSerializer
from apps.product.serializers import ProductViewSerializers
from apps.users.models  import User
from apps.product.models import Product

class SellerProfileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request: Request, pk):
        seller = get_object_or_404(SellerProfile, pk = pk)
        serializers = SellerProfileSerializer(seller)

        return Response(serializers.data)


class SellerProductsView(ListAPIView):
    serializer_class = ProductViewSerializers
    permission_classes = [AllowAny]

    def get_queryset(self):
        seller_id = self.kwargs["seller_id"]

        seller = get_object_or_404(User, id=seller_id)

        return Product.objects.select_related(
            "seller", "category"
        ).filter(
            seller=seller,
            status="aktiv"
        ).order_by("-created_at")


        