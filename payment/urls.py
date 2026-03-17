from django.urls import path
from .views import CreateStripeCheckout
app_name = 'payment'
urlpatterns = [
    path('/checkout/<int:order_id>/', CreateStripeCheckout.as_view(), name='stripe-checkout'),
]