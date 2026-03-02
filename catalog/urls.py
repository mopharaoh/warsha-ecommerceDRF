from django.urls import path
from .views import (ProductList,ProductDetail,CategoryList,
                    ProductCreate,ProductUpdate,
                    VariantUpdate,ImageUpdate,ImageCreate)
app_name='catalog'

urlpatterns=[
    path('list',ProductList.as_view(),name='productlist'),
    path('detail/<int:pk>/',ProductDetail.as_view(),name='productdetail'),
    path('category',CategoryList.as_view(),name='category'),
    path('create',ProductCreate.as_view(),name='create'),
    path('product_update/<int:pk>',ProductUpdate.as_view(),name='productupdate'),
    path('variant_update/<int:pk>',VariantUpdate.as_view(),name='variantupdate'),
    path('image_update/<int:pk>',ImageUpdate.as_view(),name='imageupdate'),
    path('image_create/',ImageCreate.as_view(),name='imagecreate'),
]