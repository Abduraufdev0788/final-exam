from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from apps.product.models import Product
from .models import Favorite
from .serializers import FavoriteSerializer


class FavoriteViews(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request:Request)->Response:

        user = request.user
        product = Favorite.objects.filter(user=user).select_related("product")
        serializer = FavoriteSerializer(product, many=True)

        return Response(serializer.data)
    
    def post(self, request:Request)-> Response:

        user = request.user
        product_id = request.data.get("product_id")

        if not product_id:
            return Response(
                {"error": "product_id kerak"},
                status=status.HTTP_400_BAD_REQUEST
            )

        product = get_object_or_404(Product, id=product_id)

        if Favorite.objects.filter(user=user, product=product).exists():
            return Response(
                {"error": "Bu product allaqachon sevimlilarga qo'shilgan"},
                status=status.HTTP_400_BAD_REQUEST
            )

        favorite = Favorite.objects.create(
            user=user,
            product=product
        )

        product.favorite_count += 1
        product.save(update_fields=["favorite_count"])

        serializer = FavoriteSerializer(favorite)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


class FavoriteDelete(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request: Request, pk) -> Response:

        favorite = get_object_or_404(
            Favorite,
            id=pk,
            user=request.user
        )

        product = favorite.product

        favorite.delete()

        product.favorite_count -= 1
        product.save(update_fields=["favorite_count"])

        return Response(status=status.HTTP_204_NO_CONTENT)
            