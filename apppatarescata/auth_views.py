from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404

from .auth_serializers import (
    LoginSerializer,
    RegistroAdoptanteSerializer,
    RegistroFundacionSerializer,
    UsuarioSerializer
)
from .models import Usuario


class LoginAPI(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            
            # Usar o crear token
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                "token": token.key,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "nombre": user.nombre,
                    "es_fundacion": bool(user.rut_empresa),
                    "is_staff": user.is_staff
                }
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        if hasattr(request.user, 'auth_token'):
            request.user.auth_token.delete()
        logout(request)
        return Response({"detail": "Sesión cerrada correctamente."})


class RegistroAdoptanteAPI(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = RegistroAdoptanteSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Enviar correo de verificación
            subject = "Verifica tu cuenta en PataRescata"
            message = f"¡Gracias por registrarte en PataRescata!\n\nPara verificar tu cuenta, haz clic en el siguiente enlace:\n{request.build_absolute_uri('/verificar-cuenta/')}{user.token_verificacion}"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]
            
            try:
                send_mail(subject, message, from_email, recipient_list)
            except Exception as e:
                # Log error but continue
                print(f"Error enviando email: {str(e)}")
            
            return Response({
                "detail": "Usuario creado exitosamente. Por favor, verifica tu correo electrónico."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegistroFundacionAPI(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = RegistroFundacionSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Enviar correo de verificación
            subject = "Verifica tu cuenta de Fundación en PataRescata"
            message = f"¡Gracias por registrar tu fundación en PataRescata!\n\nPara verificar tu cuenta, haz clic en el siguiente enlace:\n{request.build_absolute_uri('/verificar-cuenta/')}{user.token_verificacion}"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]
            
            try:
                send_mail(subject, message, from_email, recipient_list)
            except Exception as e:
                # Log error but continue
                print(f"Error enviando email: {str(e)}")
            
            return Response({
                "detail": "Fundación creada exitosamente. Por favor, verifica tu correo electrónico."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def verificar_cuenta_api(request, token):
    try:
        user = Usuario.objects.get(token_verificacion=token)
        if not user.email_verificado:
            user.email_verificado = True
            user.save()
            return Response({"detail": "¡Cuenta verificada exitosamente! Ahora puedes iniciar sesión."})
        return Response({"detail": "Esta cuenta ya ha sido verificada."})
    except Usuario.DoesNotExist:
        return Response({"error": "Token de verificación inválido."}, status=status.HTTP_400_BAD_REQUEST)


class PerfilUsuarioAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        serializer = UsuarioSerializer(request.user, context={"request": request})
        return Response(serializer.data)
    
    def put(self, request):
        serializer = UsuarioSerializer(request.user, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def eliminar_cuenta_api(request):
    user = request.user
    user.is_active = False
    user.save()
    logout(request)
    return Response({"detail": "Cuenta desactivada correctamente."})
