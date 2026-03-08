from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category,Product,Brand,ProductImage,ProductVariant
from .serializers import( ProductSerializer,VariantSerializer,
                         ImageSerializer,ProductDetailSerializer,
                         CategorySerializer,BrandSerializer,ProductCreateSerializer)
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework.permissions import AllowAny,BasePermission,SAFE_METHODS,IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

class IsBrandOwner(BasePermission):
    message='Editing product is restricted to the brand owner only.'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if isinstance(obj, Product):
            return obj.brand.owner == request.user
        elif isinstance(obj, ProductVariant):
            return obj.product.brand.owner == request.user
        elif isinstance(obj, ProductImage):
            return obj.variant.product.brand.owner == request.user
        return False


class ProductList(generics.ListAPIView):
    permission_classes = [AllowAny]
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

class CategoryList(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class BrandCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class BrandList(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProductDetail(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


class ProductCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer

class ProductUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsBrandOwner]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class VariantCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    
    serializer_class = VariantSerializer

class VariantUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsBrandOwner]
    queryset = ProductVariant.objects.all()
    serializer_class = VariantSerializer


class ImageUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsBrandOwner]
    queryset = ProductImage.objects.all()
    serializer_class =ImageSerializer
    parser_classes = [MultiPartParser, FormParser]

class ImageCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsBrandOwner]
    queryset = ProductImage.objects.all()
    serializer_class =ImageSerializer
    parser_classes = [MultiPartParser, FormParser]