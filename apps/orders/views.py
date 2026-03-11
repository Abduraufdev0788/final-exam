from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Order
from apps.product.models import Product
from .serializers import OrderSerializer


class OrderViews(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        role = request.query_params.get("role")

        if role == "seller":
            orders = Order.objects.filter(seller=request.user)

        else:
            orders = Order.objects.filter(buyer=request.user)

        serializer = OrderSerializer(orders, many=True)

        return Response(serializer.data)

    def post(self, request):

        user = request.user
        product_id = request.data.get("product_id")
        notes = request.data.get("notes", "")

        if not product_id:
            return Response(
                {"error": "product_id kerak"},
                status=status.HTTP_400_BAD_REQUEST
            )

        product = get_object_or_404(Product, id=product_id)

        order = Order.objects.create(
            product=product,
            buyer=user,
            seller=product.seller,
            final_price=product.price,
            notes=notes,
            status="Kutilyapti"
        )

        serializer = OrderSerializer(order)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        order = get_object_or_404(Order, id=pk)

        if order.buyer != request.user and order.seller != request.user:
            return Response({"error": "Ruxsat yo'q"}, status=403)

        serializer = OrderSerializer(order)
        return Response(serializer.data)


    def patch(self, request, pk):
        order = get_object_or_404(Order, id=pk)

        status_value = request.data.get("status")

        if request.user == order.seller:

            if status_value not in ["kelishilgan", "bekor qilingan"]:
                return Response({"error": "Noto'g'ri status"}, status=400)

            order.status = status_value

            if status_value == "kelishilgan":
                order.meeting_location = request.data.get("meeting_location")
                order.meeting_time = request.data.get("meeting_time")

            order.save()
            serializer = OrderSerializer(order)
            return Response(serializer.data)

        if request.user == order.buyer:

            if status_value not in ["sotib olingan", "bekor qilingan"]:
                return Response({"error": "Noto'g'ri status"}, status=400)

            order.status = status_value
            order.save()

            if status_value == "sotib olingan":
                product = order.product
                product.status = "sotilgan"
                product.save()

            serializer = OrderSerializer(order)
            return Response(serializer.data)

        return Response({"error": "Ruxsat yo'q"}, status=403)