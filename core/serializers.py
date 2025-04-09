from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User


class UserLoginSerializer(TokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD

    def validate(self, attrs):
        credentials = {
            'email': attrs.get('email'),
            'password': attrs.get('password')
        }

        user = User.objects.filter(email=credentials['email']).first()
        if user and user.check_password(credentials['password']):
            token = self.get_token(user)
            return {
                'email': user.email,
                'access': str(token.access_token),
            }

        raise serializers.ValidationError('Invalid email or password')
