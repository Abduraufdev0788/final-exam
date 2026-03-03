from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.request import Request
from .models import User
from .serializers import UserSerializer, UserUpdateSerializer, UpgradeToSellerSerializer

class MeView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request:Request):
        user = request.user
        serializers = UserSerializer(user)
        return Response(serializers.data)
    
    def patch(self, request: Request):
        user = request.user
        serializers = UserUpdateSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.update(user, serializers.validated_data)
        return Response(UserSerializer(user).data)
    
class UpgradeToSeller(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request:Request):
        serializers = UpgradeToSellerSerializer(data = request.data, context = {"request": request})
        serializers.is_valid(raise_exception=True)
        seller_profile = serializers.save()

        return Response({"message":"Siz endi sotuvchisiz", "shop_name":seller_profile.shop_name})


