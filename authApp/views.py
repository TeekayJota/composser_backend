#authApp/views.py
from rest_framework import permissions, status, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomUserSerializer, CustomTokenObtainPairSerializer, ChangePasswordSerializer


# Vista personalizada para obtener el par de tokens (access y refresh)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# Vista para ver y actualizar el perfil del usuario autenticado
class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = CustomUserSerializer(user, data=request.data,
                                          partial=True)  # partial=True permite actualizar parcialmente
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vista para cambiar la contraseña del usuario autenticado
class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Verificar la contraseña actual
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({"old_password": ["La contraseña actual no es correcta."]},
                                status=status.HTTP_400_BAD_REQUEST)

            # Establecer la nueva contraseña
            user.set_password(serializer.validated_data['new_password'])
            user.save()

            return Response({"detail": "La contraseña ha sido cambiada exitosamente."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]
