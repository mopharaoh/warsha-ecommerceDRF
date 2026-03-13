from django.urls import path
from .views import CheckoutOrder,OrderHistory

app_name = 'Order'
urlpatterns = [
    path('',CheckoutOrder.as_view(),name='order'),
    path('/history/',OrderHistory.as_view(),name='history'),
]