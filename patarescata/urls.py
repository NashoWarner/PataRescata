from django.contrib import admin
from django.urls import path
from apppatarescata import views

from apppatarescata.views import (
    faq, home, blog, nosotros, preguntas_frecuentes, agregarMascota, 
    buscar_animales, resultado_busqueda, registro_usuario, mi_login, 
    logout_view, info_perfil, articulo1, articulo2, articulo3, articulo4, 
    articulo5, navegador, home_perfil, actualizar_perfil, eliminar_cuenta, 
    realizar_adopcion, mis_solicitudes, verificar_cuenta, tienda  # Asegúrate de importar la vista de la tienda
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('preguntas-frecuentes/', preguntas_frecuentes, name='preguntas_frecuentes'),
    path('admin/', admin.site.urls),
    path('navegador/', navegador),
    path('blog/', blog),
    path('articulo5/', articulo5),
    path('articulo4/', articulo4),
    path('articulo3/', articulo3),
    path('articulo2/', articulo2),
    path('articulo1/', articulo1),
    path('nosotros/', faq),
    path('faq/', faq, name='faq'),
    path('realizar_adopcion/<int:animal_id>/', realizar_adopcion, name='realizar_adopcion'),
    path('mis_solicitudes/', mis_solicitudes, name='mis_solicitudes'),
    path('', home),
    path('tienda/', tienda, name='tienda'),  # Nueva ruta para la tienda
    path('home_perfil/', info_perfil, name='home_perfil'), 
    path('agregarmascota/', agregarMascota, name='agregarmascota'),
    path('buscar_animales/', buscar_animales, name='buscar_animales'),
    path('resultado_busqueda/', resultado_busqueda, name='resultado_busqueda'),
    path('login/', mi_login, name='mi_login'), 
    path('registro/', registro_usuario, name='registro_usuario'),
    path('logout/', logout_view, name='logout'),
    path('actualizar_perfil/', actualizar_perfil, name='actualizar_perfil'),
    path('eliminar-cuenta/', eliminar_cuenta, name='eliminar_cuenta'),
    path('verificar-cuenta/<str:token>/', verificar_cuenta, name='verificar-cuenta'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
