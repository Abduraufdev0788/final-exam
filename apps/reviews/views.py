from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Avg

from .models import Review
from .serializers import ReviewSerializer
from apps.orders.models import Order
from apps.sellers.models import SellerProfile


class ReviewViews(APIView):

    def get(self, request):
        seller_id = request.query_params.get("seller_id")

        reviews = Review.objects.all()

        if seller_id:
            reviews = reviews.filter(seller_id=seller_id)

        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request):

        order_id = request.data.get("order_id")
        rating = request.data.get("rating")
        comment = request.data.get("comment", "")

        order = get_object_or_404(Order, id=order_id)

        if order.buyer != request.user:
            return Response({"error": "Faqat buyer review yozadi"}, status=403)

        if order.status != "sotib olingan":
            return Response({"error": "Order hali yakunlanmagan"}, status=400)

        if Review.objects.filter(order=order).exists():
            return Response({"error": "Bu order uchun review yozilgan"}, status=400)

        review = Review.objects.create(
            order=order,
            reviewer=request.user,
            seller=order.seller,
            rating=rating,
            comment=comment
        )

        avg_rating = Review.objects.filter(seller=order.seller).aggregate(avg=Avg("rating"))["avg"]

        seller_profile = SellerProfile.objects.get(user=order.seller)
        seller_profile.rating = avg_rating
        seller_profile.save(update_fields=["rating"])

        serializer = ReviewSerializer(review)

        return Response(serializer.data, status=status.HTTP_201_CREATED)