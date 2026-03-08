from django.urls import path
from .views import (ProductList,ProductDetail,CategoryList,
                    ProductCreate,ProductUpdate,
                    VariantUpdate,ImageUpdate,ImageCreate,
                    VariantCreate,BrandList,BrandCreate)
app_name='catalog'

urlpatterns=[
    # Category
    path('categories/', CategoryList.as_view(), name='category-list'),
    #brand
    path('brands/',BrandList.as_view(),name = 'brands'),
    path('brands/create/',BrandCreate.as_view(),name = 'brandcreate'),
    # Product
    path('products/', ProductList.as_view(), name='product-list'),
    path('products/create/', ProductCreate.as_view(), name='product-create'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('products/<int:pk>/update/', ProductUpdate.as_view(), name='product-update'),
    
    # Variant
    path('variants/create/', VariantCreate.as_view(), name='variant-create'),
    path('variants/<int:pk>/update/', VariantUpdate.as_view(), name='variant-update'), 
    
    # Image
    path('images/create/', ImageCreate.as_view(), name='image-create'),
    path('images/<int:pk>/update/', ImageUpdate.as_view(), name='image-update'),
]