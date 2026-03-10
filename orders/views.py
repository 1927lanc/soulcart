from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from .serializers import OrderSerializer
from cart.models import Cart, CartItem


class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        address = request.data.get('address')
        if not address:
            return Response({'error': 'Address is required'}, status=400)

        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.items.all()
            if not cart_items:
                return Response({'error': 'Cart is empty'}, status=400)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=404)

        total = sum(item.quantity * item.product.price for item in cart_items)

        order = Order.objects.create(
            user=request.user,
            address=address,
            total_price=total,
            status='pending'
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        cart_items.delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=201)


class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=404)
        serializer = OrderSerializer(order)
        return Response(serializer.data)