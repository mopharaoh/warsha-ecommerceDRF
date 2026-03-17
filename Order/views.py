from django.shortcuts import render
from rest_framework.views import APIView
from .models import Order,OrderItem
from .serializers import OrderSerializer,CheckoutSerializer,OrderUpdateSerializer
from cart.models import Cart,CartItem
from catalog.models import ProductVariant
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.db import transaction
from rest_framework.generics import ListAPIView, UpdateAPIView
from decimal import Decimal

class CheckoutOrder(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = CheckoutSerializer(data=request.data)
        if serializer.is_valid():
            
            shipping_address = serializer.validated_data['shipping_address']
            shipping_phone = serializer.validated_data.get('shipping_phone',request.user.phone)
            user=request.user
            try:
                cart=Cart.objects.get(user=user)
            except Cart.DoesNotExist:
                return Response({"error": "You do not have an active cart."}, status=status.HTTP_400_BAD_REQUEST)
            
            if not cart.items.exists():
                return Response({"error":"Your cart is empty."},status=status.HTTP_400_BAD_REQUEST)
            
            try:
                with transaction.atomic():
                    shipping_cost = Decimal(50.00)
                    order = Order.objects.create(
                        user=user,
                        shipping_price=shipping_cost,
                        total_amount=cart.total_price + shipping_cost,
                        shipping_address=shipping_address,
                        shipping_phone=shipping_phone
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
    

class OrderUpdate(UpdateAPIView):
    serializer_class = OrderUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def perform_update(self, serializer):
        
        order = self.get_object()

        if order.status != 'Pending':
            raise ValidationError({"error": "You cannot update or cancel this order because it is already being processed or shipped."})
        new_status = serializer.validated_data.get('status')
        if new_status and new_status!= 'Cancelled':
            raise ValidationError({"error": "You are only allowed to cancel the order."})
        if new_status == 'Cancelled' and order.status != 'Cancelled':
            with transaction.atomic():
                for item in order.items.all():
                    if item.variant:
                        item.variant.stock += item.quantity
                        item.variant.save()
                serializer.save()
        else:
            serializer.save()