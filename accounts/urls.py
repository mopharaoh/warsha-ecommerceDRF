from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView
from django.urls import path
from .views import RegisterView,LogoutView,LoginView
app_name = 'accounts'
urlpatterns = [
    path('/register',RegisterView.as_view(),name='register'),
    path('/login/', LoginView.as_view(), name='login'),
    path('/logout',LogoutView.as_view(),name='logout'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh')
]