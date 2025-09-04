from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import Usuario

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        user = authenticate(
            email=data.get('email'),
            password=data.get('password')
        )
        
        if not user:
            raise serializers.ValidationError("Credenciales incorrectas. Intente de nuevo.")
        
        if not user.email_verificado and user.is_active:
            raise serializers.ValidationError("Por favor, verifique su correo electrónico antes de iniciar sesión.")
            
        return {
            'user': user,
            'email': user.email,
            'nombre': user.nombre,
            'is_staff': user.is_staff,
            'id': user.id,
            'es_fundacion': bool(user.rut_empresa),
        }

class RegistroAdoptanteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = Usuario
        fields = ['email', 'nombre', 'telefono', 'password', 'password_confirm']
        
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = Usuario.objects.create_user(
            email=validated_data['email'],
            nombre=validated_data['nombre'],
            telefono=validated_data['telefono'],
            password=validated_data['password'],
            token_verificacion=Usuario._meta.get_field('token_verificacion').get_default()
        )
        return user

class RegistroFundacionSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = Usuario
        fields = ['email', 'nombre', 'telefono', 'rut_empresa', 'password', 'password_confirm']
        
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = Usuario.objects.create_user(
            email=validated_data['email'],
            nombre=validated_data['nombre'],
            telefono=validated_data['telefono'],
            rut_empresa=validated_data['rut_empresa'],
            password=validated_data['password'],
            token_verificacion=Usuario._meta.get_field('token_verificacion').get_default()
        )
        return user

class UsuarioSerializer(serializers.ModelSerializer):
    imagen_perfil_url = serializers.SerializerMethodField()
    es_fundacion = serializers.SerializerMethodField()
    
    class Meta:
        model = Usuario
        fields = ['id', 'email', 'nombre', 'telefono', 'rut_empresa', 'imagen_perfil', 
                 'imagen_perfil_url', 'email_verificado', 'es_fundacion']
        read_only_fields = ['email', 'email_verificado']
        
    def get_imagen_perfil_url(self, obj):
        request = self.context.get('request')
        if obj.imagen_perfil and hasattr(obj.imagen_perfil, 'url'):
            if request:
                return request.build_absolute_uri(obj.imagen_perfil.url)
            return obj.imagen_perfil.url
        return None
    
    def get_es_fundacion(self, obj):
        return bool(obj.rut_empresa)
