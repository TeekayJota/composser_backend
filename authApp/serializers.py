#authApp/serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

CustomUser = get_user_model()


# Serializer para la creación y visualización de los usuarios.
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email',
            'phone_number', 'acknowledge_level', 'role', 'instrument',
            'interests', 'address'
        ]
        extra_kwargs = {
            'password': {'write_only': True}  # Asegura que la contraseña no sea visible.
        }


# Serializer para el Token JWT con campos personalizados.
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Agregar campos adicionales al token
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['role'] = user.role
        token['instrument'] = user.instrument
        return token


# Serializer para cambiar la contraseña.
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
