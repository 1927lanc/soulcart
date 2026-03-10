from django.contrib.auth import authenticate
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import User, Wishlist
from .serializers import UserSerializer
from products.models import Product
from products.serializers import ProductSerializer

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        if User.objects.filter(username=data.get('username')).exists():
            return Response({'error': 'Username already exists'}, status=400)
        if User.objects.filter(email=data.get('email')).exists():
            return Response({'error': 'Email already exists'}, status=400)
        user = User.objects.create_user(
            username=data.get('username'),
            email=data.get('email'),
            password=data.get('password'),
            phone=data.get('phone', '')
        )
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': {'id': user.id, 'username': user.username, 'email': user.email}
        }, status=201)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': {'id': user.id, 'username': user.username, 'email': user.email}
            })
        return Response({'error': 'Invalid username or password'}, status=400)


class LogoutView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            request.user.auth_token.delete()
        return Response({'message': 'Logged out successfully'})


class ProfileView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Not authenticated'}, status=401)
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class WishlistView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        wishlist = Wishlist.objects.filter(user=request.user).select_related('product')
        products = [w.product for w in wishlist]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        product_id = request.data.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
            wishlist, created = Wishlist.objects.get_or_create(user=request.user, product=product)
            if created:
                return Response({'message': 'Added to wishlist'}, status=201)
            else:
                wishlist.delete()
                return Response({'message': 'Removed from wishlist'}, status=200)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)