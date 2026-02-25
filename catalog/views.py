from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category,Product,ProductImage,ProductVariant
from .serializers import ProductSerializer,VariantSerializer,ImageSerializer,ProductDetailSerializer,CategorySerializer
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend 


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    search_fields = ['name', 'description']
    ordering_fields = ['variants__price']

    filterset_fields = {
        'category__slug': ['exact'],
        'brand__name': ['exact'],
        'is_bundle': ['exact'],
        'variants__price': ['gte', 'lte'],
    }
class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
