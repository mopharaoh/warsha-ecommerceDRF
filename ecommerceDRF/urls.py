from django.contrib import admin
from django.urls import path,include
from . import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("catalog.urls",namespace='catalog')),
    path('account',include('accounts.urls',namespace='accounts')),
    path('cart',include('cart.urls',namespace='cart')),
    path('order',include("Order.urls",namespace='Order')),
    path('payment',include("payment.urls",namespace='payment')),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
