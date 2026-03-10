from rest_framework import serializers
from .models import CartItem,Cart

class CartItemSerializer(serializers.ModelSerializer):

    sub_total = serializers.ReadOnlyField()

    variant_name = serializers.CharField(source='variant.product.name',read_only=True)
    price = serializers.DecimalField(source='variant.price',max_digits=10,decimal_places=2,read_only=True)

    class Meta:
        model = CartItem
        fields=['id','variant','variant_name','price','quantity','sub_total']


class CartSerializer(serializers.ModelSerializer):

    items = CartItemSerializer(many=True,read_only=True)

    total_price = serializers.ReadOnlyField()
    coupon = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id','user','created_at','items','coupon','total_price']

class ApplyCouponSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=100)