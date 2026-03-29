from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView
from django.urls import path
from .views import (RegisterView,LogoutView,
                    UserProfileView,LoginView,
                    RequestOTPView,VerifyOTPView,
                    ChangePasswordView,ResetPasswordView,
                    GoogleLoginView)
app_name = 'accounts'
urlpatterns = [
    path('/register',RegisterView.as_view(),name='register'),
    path('/login/', LoginView.as_view(), name='login'),
    path('/google-login/', GoogleLoginView.as_view(), name='google-login'),
    path('/profile/',UserProfileView.as_view(),name='user-profile'),
    path('/change-password/',ChangePasswordView.as_view(),name='change-password'),
    
    path('/logout',LogoutView.as_view(),name='logout'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    
    path('/password-reset/request-otp/',RequestOTPView.as_view(),name='request-otp'),
    path('/password-reset/verify-otp/',VerifyOTPView.as_view(),name='verify-otp'),
    path('/password-reset/confirm/',ResetPasswordView.as_view(),name='reset-password')
]