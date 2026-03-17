from django.urls import path
from .views import CheckoutOrder,OrderHistory,OrderUpdate

app_name = 'Order'
urlpatterns = [
    path('',CheckoutOrder.as_view(),name='order'),
    path('/history/',OrderHistory.as_view(),name='history'),
    path('/<int:id>/update/',OrderUpdate.as_view(),name='update')
]