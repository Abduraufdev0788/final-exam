from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import Request
from django.shortcuts import get_object_or_404
from .models import SellerProfile
from .serializers import SellerProfileSerializer

class SellerProfileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request: Request, pk):
        seller = get_object_or_404(SellerProfile, pk = pk)
        serializers = SellerProfileSerializer(seller)

        return Response(serializers.data)



        