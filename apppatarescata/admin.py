from django.contrib import admin
from django.utils import timezone

from apppatarescata.models import Producto



@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio', 'enlace']
    list_filter = ['categoria']
    search_fields = ['nombre', 'descripcion']
    readonly_fields = []
    fieldsets = (
        ('Información del Producto', {
            'fields': ('nombre', 'descripcion', 'precio', 'imagen', 'enlace', 'categoria')
        }),
    )
