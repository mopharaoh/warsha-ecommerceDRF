from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenSerializer(TokenObtainPairSerializer):

    def validate(self,attrs):
        data = super().validate(attrs)

        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'username': self.user.user_name,
            'is_vendor': self.user.is_vendor
        }
        return data
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'user_name', 'first_name', 'last_name', 'phone', 'address']
        read_only_fields = ['id' , 'email' , 'user_name']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email','user_name','first_name',
                  'last_name','password','is_vendor','phone','address']
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)