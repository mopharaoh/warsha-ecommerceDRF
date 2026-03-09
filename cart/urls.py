from django.urls import path
from .views import AddCartItem,CartDetail,CartItemUpdate

app_name = 'cart'

urlpatterns = [
    path('/add/',AddCartItem.as_view(),name='additem'),
    path('/detail/',CartDetail.as_view(),name='cartdetail'),
    path('/item/<int:pk>/update/',CartItemUpdate.as_view(),name='cartItemupdate')
]