from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .serializers import RegisterSerializer,CustomTokenSerializer,UserProfileSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, generics
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User,PasswordResetOTP
import random
from django.core.mail import send_mail
from ecommerceDRF import settings
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import os
from .tasks import send_otp_email_task

class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer

class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):

        token = request.data.get('id_token')

        if not token:
            return Response({"error": "No token provided"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            client_id = os.environ.get('GOOGLE_CLIENT_ID')
            idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), client_id)
            
            
            email = idinfo.get('email')
            first_name = idinfo.get('given_name', '')
            last_name = idinfo.get('family_name', '')
            base_username = email.split('@')[0]
            user = User.objects.filter(email=email).first()
            if not user:
                user = User.objects.create(email=email,
                                    user_name=base_username,
                                    first_name=first_name,
                                    last_name=last_name
                                    )
                user.set_unusable_password()
                user.save()
            refresh = RefreshToken.for_user(user)
            return Response({"refresh_token":str(refresh),
                             "access_token":str(refresh.access_token)},
                             status=status.HTTP_200_OK)

        except ValueError:
            return Response({"error": "Invalid Google token"}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user

class RequestOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):

        email = request.data.get('email')
        if not email:
            return Response({"error": "Please provide an email address."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Sorry, this email doesn't exist."}, status=status.HTTP_404_NOT_FOUND)
        code = str(random.randint(100000, 999999))
        PasswordResetOTP.objects.update_or_create(user=user,defaults={'otp_code':code})
        subject = f"{user.user_name}'s OTP for Password reset"
        message = f"Hello here is your OTP >> {code}\n\nThis code is valid for 10 minutes."
        
        send_otp_email_task.delay(subject,message,email,code)
        
        return Response({"message": "OTP sent successfully to your email..."}, status=status.HTTP_200_OK)


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        email = request.data.get('email')
        otp_code= request.data.get('otp_code')

        if not email or not otp_code:
            return Response({"error": "Please provide both email and OTP."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error":"User not found."},status=status.HTTP_400_BAD_REQUEST)
        try:
            otp_record = PasswordResetOTP.objects.get(user=user,otp_code=otp_code)
        except PasswordResetOTP.DoesNotExist:
            return Response({"error": "Invalid OTP code."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not otp_record.is_valid():

            otp_record.delete()
            return Response({"error": "OTP has expired. Please request a new one."}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"success": "OTP verified successfully. You can now reset your password."}, status=status.HTTP_200_OK)

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):

        email = request.data.get('email')
        otp_code=request.data.get('otp_code')
        new_password = request.data.get('new_password')

        if not new_password or len(new_password) < 8:
            return Response(
                {"error": "Password must be at least 8 characters long."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error":"User not found."},status=status.HTTP_400_BAD_REQUEST)
        try:
            otp_record = PasswordResetOTP.objects.get(user=user,otp_code=otp_code)
        except PasswordResetOTP.DoesNotExist:
            return Response({"error": "Invalid OTP code."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not otp_record.is_valid():
            otp_record.delete()
            return Response({"error": "OTP has expired. Please request a new one."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.set_password(new_password)
            user.save()
            otp_record.delete()
            return Response({"success": "You just Reset your Password successfully."}, status=status.HTTP_200_OK)

class ChangePasswordView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self,request):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not new_password or len(new_password) < 8:
            return Response(
                {"error": "Password must be at least 8 characters long."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if not request.user.check_password(old_password):
            return Response({"error": "Invalid old password."}, status=status.HTTP_400_BAD_REQUEST)
        
        request.user.set_password(new_password)
        request.user.save()
        return Response({"success": " Password changed successfully."}, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message":"logged out..."},status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid token"},status=status.HTTP_400_BAD_REQUEST)
