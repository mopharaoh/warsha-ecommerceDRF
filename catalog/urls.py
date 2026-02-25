from django.urls import path
from .views import ProductList,ProductDetail,CategoryList

app_name='catalog'

urlpatterns=[
    path('list',ProductList.as_view(),name='productlist'),
    path('detail/<int:pk>/',ProductDetail.as_view(),name='productdetail'),
    path('category',CategoryList.as_view(),name='category'),
    # path('create',ProductCreate.as_view(),name='create')
]