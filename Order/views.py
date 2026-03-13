from django.shortcuts import render
from rest_framework.views import APIView
from .models import Order,OrderItem
from .serializers import OrderSerializer,CheckoutSerializer
from cart.models import Cart,CartItem
from catalog.models import ProductVariant
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.db import transaction
from rest_framework.generics import ListAPIView

class CheckoutOrder(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = CheckoutSerializer(data=request.data)
        if serializer.is_valid():
            
            shipping_address = serializer.validated_data['shipping_address']
            user=request.user
            try:
                cart=Cart.objects.get(user=user)
            except Cart.DoesNotExist:
                return Response({"error": "You do not have an active cart."}, status=status.HTTP_400_BAD_REQUEST)
            
            if not cart.items.exists():
                return Response({"error":"Your cart is empty."},status=status.HTTP_400_BAD_REQUEST)
            
            try:
                with transaction.atomic():

                    order = Order.objects.create(
                        user=user,
                        total_amount=cart.total_price,
                        shipping_address=shipping_address
                    )
            
                    for cart_item in cart.items.all():
                        variant = cart_item.variant

                        if variant.stock < cart_item.quantity:
                            raise ValidationError(f"Sorry, not enough stock for {variant.product.name}")
                        
                        OrderItem.objects.create(order=order,
                                                variant=variant,
                                                price=variant.price,
                                                quantity=cart_item.quantity
                                                )
                        variant.stock -= cart_item.quantity
                        variant.save()
                    cart.delete()
                order_serializer = OrderSerializer(order)
                return Response({
                        "message": "Order placed successfully!",
                        "order": order_serializer.data
                    }, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({"error": str(e.detail[0])}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                

class OrderHistory(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user).order_by('-created_at')