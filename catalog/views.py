from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category,Product,ProductImage,ProductVariant
from .serializers import ProductSerializer,VariantSerializer,ImageSerializer,ProductCreateSerializer,ProductDetailSerializer,CategorySerializer
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend 


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all().order_by('id').distinct()
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

class ProductCreate(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer

class ProductUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
class VariantUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductVariant.objects.all()
    serializer_class = VariantSerializer
class ImageUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductImage.objects.all()
    serializer_class =ImageSerializer

class ImageCreate(generics.CreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class =ImageSerializer