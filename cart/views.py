from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from .models import Cart,CartItem,Coupon
from .serializers import CartItemSerializer,CartSerializer,ApplyCouponSerializer
from rest_framework.permissions import AllowAny , IsAuthenticated 
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status

class AddCartItem(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        cart,created = Cart.objects.get_or_create(user=self.request.user)

        variant = serializer.validated_data['variant']
        quantity = serializer.validated_data.get('quantity',1)

        existing_item = CartItem.objects.filter(cart=cart,variant=variant).first()

        total_requested_quantity = quantity
        if existing_item:
            total_requested_quantity +=existing_item.quantity

        if total_requested_quantity > variant.stock:
            raise ValidationError({
                "error":f"Sorry, only {variant.stock} items are available in stock."
            })

        if existing_item:
            existing_item.quantity =total_requested_quantity
            existing_item.save()

        else:
            serializer.save(cart=cart)

class CartDetail(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart,created = Cart.objects.get_or_create(user=self.request.user)
        return cart
    

class CartItemUpdate(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)
    
    def perform_update(self, serializer):

        item = serializer.instance
        variant = item.variant

        new_quantity = serializer.validated_data.get('quantity',item.quantity)

        if new_quantity> variant.stock:
            raise ValidationError({
                "error":f"Sorry, you cannot update. only {variant.stock} items are available in stock."
            })
        serializer.save()


class ApplyCouponView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self,request):

        serializer = ApplyCouponSerializer(data=request.data)

        if serializer.is_valid():
            code = serializer.validated_data['code']

            try:
                coupon = Coupon.objects.get(code=code)
                if not coupon.valid:
                    return Response({
                        "error":"This coupon is expired or invalid."
                    },status=status.HTTP_400_BAD_REQUEST)
                
                cart, _ =Cart.objects.get_or_create(user=request.user)

                if coupon.brand:

                    brand_in_cart = cart.items.filter(variant__product__brand=coupon.brand).exists()
                    if not brand_in_cart:
                        return Response({
                            "error": f"This coupon is only valid for {coupon.brand.name} products, which are not in your cart."
                        }, status=status.HTTP_400_BAD_REQUEST)
                cart.coupon = coupon
                cart.save()

                cart_serializer = CartSerializer(cart)
                return Response({
                    "message": "Coupon applied successfully!",
                    "cart": cart_serializer.data
                }, status=status.HTTP_200_OK)
            except Coupon.DoesNotExist:
                return Response(
                    {"error": "Invalid coupon code."}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)