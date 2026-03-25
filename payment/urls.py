from django.urls import path
from .views import CreateStripeCheckout,stripe_webhook
app_name = 'payment'
urlpatterns = [
    path('/checkout/<int:order_id>/', CreateStripeCheckout.as_view(), name='stripe-checkout'),
    path('/webhook/',stripe_webhook,name = 'stripe-webhook')
]