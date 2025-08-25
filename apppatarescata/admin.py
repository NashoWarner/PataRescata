from django.contrib import admin
from .models import Mascota, FAQ, Usuario, Adopcion, Producto

@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ('nombre_mascota', 'edad_mascota', 'tamaño_mascota', 'comuna_mascota', 'region', 'adopcion_solicitada')
    list_filter = ('tamaño_mascota', 'comuna_mascota', 'region', 'adopcion_solicitada')
    search_fields = ('nombre_mascota', 'descripcion')
    list_per_page = 20
    ordering = ('nombre_mascota',)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('pregunta',)
    search_fields = ('pregunta', 'respuesta')

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('email', 'nombre', 'telefono', 'is_staff', 'email_verificado')
    list_filter = ('is_staff', 'is_superuser', 'email_verificado')
    search_fields = ('email', 'nombre', 'telefono')
    ordering = ('email',)

@admin.register(Adopcion)
class AdopcionAdmin(admin.ModelAdmin):
    list_display = ('adoptante', 'mascota', 'fecha_adopcion', 'solicitada')
    list_filter = ('solicitada', 'fecha_adopcion')
    search_fields = ('adoptante__nombre', 'mascota__nombre_mascota')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'categoria')
    list_filter = ('categoria',)
    search_fields = ('nombre', 'descripcion')
    list_per_page = 20
    ordering = ('nombre',)
    fieldsets = (
        ('Información básica', {
            'fields': ('nombre', 'descripcion', 'precio')
        }),
        ('Detalles adicionales', {
            'fields': ('imagen', 'enlace', 'categoria')
        }),
    )

