from django.contrib import admin
from django.utils import timezone

from apppatarescata.models import Producto, NewsletterSubscription



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


@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['email', 'fecha_suscripcion', 'activo', 'confirmado']
    list_filter = ['activo', 'confirmado', 'fecha_suscripcion']
    search_fields = ['email']
    readonly_fields = ['fecha_suscripcion', 'token_confirmacion']
    fieldsets = (
        ('Información de Suscripción', {
            'fields': ('email', 'fecha_suscripcion', 'activo', 'confirmado')
        }),
        ('Configuración Técnica', {
            'fields': ('token_confirmacion',),
            'classes': ('collapse',)
        }),
    )
