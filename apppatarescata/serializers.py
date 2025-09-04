from rest_framework import serializers
from .models import Mascota, Producto, ArticuloBlog, Adopcion


class MascotaSerializer(serializers.ModelSerializer):
    imagen_url = serializers.SerializerMethodField()
    class Meta:
        model = Mascota
        fields = [
            'id', 'nombre_mascota', 'edad_mascota', 'tipo_mascota', 'tamaño_mascota',
            'comuna_mascota', 'region', 'descripcion', 'imagen', 'imagen_url', 'adopcion_solicitada',
            'disponible'
        ]

    def get_imagen_url(self, obj):
        request = self.context.get('request')
        if obj.imagen and hasattr(obj.imagen, 'url'):
            if request:
                return request.build_absolute_uri(obj.imagen.url)
            return obj.imagen.url
        return None


class ProductoSerializer(serializers.ModelSerializer):
    imagen_url = serializers.SerializerMethodField()
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'imagen', 'imagen_url', 'enlace', 'categoria']

    def get_imagen_url(self, obj):
        request = self.context.get('request')
        if obj.imagen and hasattr(obj.imagen, 'url'):
            if request:
                return request.build_absolute_uri(obj.imagen.url)
            return obj.imagen.url
        return None


class ArticuloBlogSerializer(serializers.ModelSerializer):
    autor_nombre = serializers.SerializerMethodField()

    class Meta:
        model = ArticuloBlog
        fields = [
            'id', 'titulo', 'slug', 'resumen', 'contenido', 'imagen', 'categoria',
            'fecha_publicacion', 'publicado', 'destacado', 'visitas', 'autor_nombre'
        ]

    def get_autor_nombre(self, obj):
        return getattr(obj.autor, 'nombre', None)


class AdopcionSerializer(serializers.ModelSerializer):
    mascota_nombre = serializers.ReadOnlyField(source='mascota.nombre_mascota')

    class Meta:
        model = Adopcion
        fields = [
            'id', 'adoptante', 'mascota', 'mascota_nombre', 'fecha_solicitud',
            'estado', 'fecha_resolucion', 'comentario_fundacion'
        ]
        read_only_fields = ['fecha_solicitud']
