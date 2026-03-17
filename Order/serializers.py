from rest_framework import serializers
from .models import Order,OrderItem


class OrderItemSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(source='variant.product.name',read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id','product_name','price','quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True,read_only=True)
    class Meta:
        model = Order
        fields = ['id','user','status','total_amount','shipping_address','created_at','items']


class CheckoutSerializer(serializers.Serializer):
    shipping_address = serializers.CharField(max_length=500)
    shipping_phone = serializers.CharField(max_length=20,required=False)


class OrderUpdateSerializer(serializers.ModelSerializer):

    class Meta:

        model =  Order
        fields = ['shipping_address','shipping_phone','status']