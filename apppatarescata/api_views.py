from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from .models import Mascota, Producto, ArticuloBlog, Adopcion
from .serializers import (
    MascotaSerializer,
    ProductoSerializer,
    ArticuloBlogSerializer,
    AdopcionSerializer,
)


class IsReadOnly(permissions.BasePermission):
    """Permite solo métodos de lectura."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class MascotaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Mascota.objects.all().order_by('-id')
    serializer_class = MascotaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre_mascota', 'tipo_mascota', 'comuna_mascota', 'region']

    @action(detail=False, methods=['get'])
    def disponibles(self, request):
        qs = self.get_queryset().filter(disponible=True)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class ProductoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Producto.objects.all().order_by('-id')
    serializer_class = ProductoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'categoria']


class ArticuloBlogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ArticuloBlogSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['titulo', 'categoria']

    def get_queryset(self):
        return ArticuloBlog.objects.filter(publicado=True).order_by('-fecha_publicacion', '-fecha_creacion')


class AdopcionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AdopcionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'rut_empresa', None):
            # Fundación: solicitudes de sus mascotas
            return Adopcion.objects.filter(
                mascota__mascotafundacion__adoptante=user
            ).select_related('mascota', 'adoptante').order_by('-fecha_solicitud')
        else:
            # Adoptante: sus solicitudes
            return Adopcion.objects.filter(
                adoptante=user
            ).select_related('mascota').order_by('-fecha_solicitud')
