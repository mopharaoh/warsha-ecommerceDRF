from django.contrib import admin
from django.urls import path,include
from . import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("catalog.urls",namespace='catalog')),
    path('account',include('accounts.urls',namespace='accounts')),
    path('cart',include('cart.urls',namespace='cart')),
    path('order',include("Order.urls",namespace='Order')),
    path('payment',include("payment.urls",namespace='payment')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
