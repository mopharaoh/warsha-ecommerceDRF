from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category,Product,Brand,ProductImage,ProductVariant,WishList,Review
from .serializers import( ProductSerializer,VariantSerializer,
                         ImageSerializer,ProductDetailSerializer,
                         CategorySerializer,BrandSerializer,
                         ProductCreateSerializer,WishListSerializer)
from rest_framework import generics,status
from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework.permissions import AllowAny,BasePermission,SAFE_METHODS,IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from Order.models import Order

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

class UserWishListView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WishListSerializer

    def get_object(self):
        wishlist, created = WishList.objects.get_or_create(user=self.request.user)
        return wishlist

class ToggleWishListView(APIView):
    Permission_classes = [IsAuthenticated]

    def post(self,request,product_id):

        wishlist,created = WishList.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product,id=product_id)

        if product in wishlist.products.all():
            wishlist.products.remove(product)
            action = 'removed'
            message = "Product removed from your wishlist."
        else:
            wishlist.products.add(product)
            action = 'added'
            message = "Product added to your wishlist."

        return Response({"success":True,"action":action,"message":message},status=status.HTTP_200_OK)

class ReviewRatingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request,product_id):
        product = get_object_or_404(Product,id=product_id)
        user=request.user
        
        if hasattr(product,"owner") and product.owner == user:
            return Response({
                "error":"You cannot rate your own Product."
            })
        has_bought = Order.objects.filter(user=user,
                                          status__in=['Processing', 'Shipped', 'Delivered', 'Successful'],
                                   items__variant__product=product).exists()

        if not has_bought:
            return Response({
                "error":"You must buy this product first to leave a review."
            },status=status.HTTP_403_FORBIDDEN)

        rating = request.data.get("rating")
        comment = request.data.get("comment","")

        if not rating or int(rating)< 1 or int(rating) > 5:
            return Response({"error":"Please provide a valid rating between 1 and 5."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        review , created = Review.objects.update_or_create(user=user,
                                                           product=product,
                                                           defaults={
                                                                    'rating': rating,
                                                                    'comment': comment})
        message = "Review added successfully!" if created else "Review updated successfully!"

        return Response({"success": True, "message": message}, status=status.HTTP_200_OK)
    

class DeleteReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id):
        try:
            review = Review.objects.get(product=product_id,user=request.user)
            review.delete()

            return Response({"success": True, "message": "Review deleted successfully."}, 
                status=status.HTTP_200_OK)
        except Review.DoesNotExist:
            return Response(
                {"error": "You haven't reviewed this product yet."}, 
                status=status.HTTP_404_NOT_FOUND
            )