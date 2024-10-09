# authApp/serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

CustomUser = get_user_model()


# Serializer para la creación y visualización de los usuarios.
class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True)  # Asegura que el campo 'password' sea parte del serializer y solo para escritura.

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email',
            'phone_number', 'acknowledge_level', 'role', 'instrument',
            'interests', 'address', 'password'  # Asegúrate de incluir 'password' en los campos.
        ]
        extra_kwargs = {
            'username': {'required': False},
            'acknowledge_level': {'required': False},
            'role': {'required': False},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')  # Extrae el password de los datos validados.
        user = CustomUser(**validated_data)  # Crea el usuario con los datos restantes.
        user.set_password(password)  # Establece la contraseña usando set_password para que se almacene encriptada.
        user.save()
        return user


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
