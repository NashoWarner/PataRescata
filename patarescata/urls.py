from django.contrib import admin
from django.urls import path
from apppatarescata import views
from apppatarescata.views import estadisticas
from apppatarescata.views import (
    faq, home, blog, nosotros, preguntas_frecuentes, agregarMascota, 
    mi_login, 
    logout_view, home_perfil, actualizar_perfil, actualizar_perfil_adoptante, eliminar_cuenta, 
    realizar_adopcion, mis_solicitudes, verificar_cuenta, tienda,
    eliminar_articulo, 
    cambiar_estado_articulo, seleccionar_tipo_cuenta, 
    login_adoptante, login_fundacion, registro_adoptante, registro_fundacion,
    perfil_adoptante, generar_solicitud_adopcion, preparar_adopcion,
    aprobar_solicitud_adopcion, rechazar_solicitud_adopcion, eliminar_solicitud_adopcion, eliminar_solicitud_fundacion, cuidado_animal, eventos,
    cambiar_imagen_perfil, eliminar_imagen_perfil, cambiar_estado_solicitud,

)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('preguntas-frecuentes/', preguntas_frecuentes, name='preguntas_frecuentes'),
    path('admin/', admin.site.urls),

    path('blog/', blog, name='blog'),

    path('nosotros/', nosotros, name='nosotros'),
    path('faq/', faq, name='faq'),
    path('cuidado-animal/', cuidado_animal, name='cuidado_animal'),
    path('eventos/', eventos, name='eventos'),
    path('realizar_adopcion/<int:animal_id>/', realizar_adopcion, name='realizar_adopcion'),
    path('preparar-adopcion/<int:mascota_id>/', preparar_adopcion, name='preparar_adopcion'),
    path('mis_solicitudes/', mis_solicitudes, name='mis_solicitudes'),
    path('aprobar-solicitud/<int:solicitud_id>/', aprobar_solicitud_adopcion, name='aprobar_solicitud'),
    path('rechazar-solicitud/<int:solicitud_id>/', rechazar_solicitud_adopcion, name='rechazar_solicitud'),
    path('eliminar-solicitud/<int:solicitud_id>/', eliminar_solicitud_adopcion, name='eliminar_solicitud'),
    path('eliminar-solicitud-fundacion/<int:solicitud_id>/', eliminar_solicitud_fundacion, name='eliminar_solicitud_fundacion'),
    path('cambiar-estado-solicitud/<int:solicitud_id>/', cambiar_estado_solicitud, name='cambiar_estado_solicitud'),
    path('', home, name='home'),
    path('tienda/', tienda, name='tienda'),
    path('home_perfil/', home_perfil, name='home_perfil'), 
    path('perfil-adoptante/', perfil_adoptante, name='perfil_adoptante'),
    path('generar-solicitud-adopcion/<int:mascota_id>/', generar_solicitud_adopcion, name='generar_solicitud_adopcion'),
    path('agregarmascota/', agregarMascota, name='agregarmascota'),


    path('login/', mi_login, name='mi_login'), 

    path('seleccionar-tipo/', seleccionar_tipo_cuenta, name='seleccionar_tipo_cuenta'),
    path('login-adoptante/', login_adoptante, name='login_adoptante'),
    path('login-fundacion/', login_fundacion, name='login_fundacion'),
    path('registro-adoptante/', registro_adoptante, name='registro_adoptante'),
    path('registro-fundacion/', registro_fundacion, name='registro_fundacion'),
    path('logout/', logout_view, name='logout'),
    path('actualizar_perfil/', actualizar_perfil, name='actualizar_perfil'),

    path('actualizar_perfil_adoptante/', actualizar_perfil_adoptante, name='actualizar_perfil_adoptante'),
    path('cambiar-imagen-perfil/', cambiar_imagen_perfil, name='cambiar_imagen_perfil'),
    path('eliminar-imagen-perfil/', eliminar_imagen_perfil, name='eliminar_imagen_perfil'),
    path('eliminar-cuenta/', eliminar_cuenta, name='eliminar_cuenta'),
    path('verificar-cuenta/<str:token>/', verificar_cuenta, name='verificar_cuenta'),
    path('listar_mascotas/', views.listar_mascotas, name='listar_mascotas'),
    path('eliminar_mascota/<int:mascota_id>/', views.eliminar_mascota, name='eliminar_mascota'),
    path('eliminar_mascotas/', views.eliminar_mascotas, name='eliminar_mascotas'),

    path('actualizar_mascota/<int:mascota_id>/', views.actualizar_mascota, name='actualizar_mascota'),
    path('estadisticas/', estadisticas, name='estadisticas'),


    
    # URLs para gestión del blog (solo administradores)



    path('eliminar-articulo/<int:articulo_id>/', eliminar_articulo, name='eliminar_articulo'),
    path('cambiar-estado-articulo/<int:articulo_id>/', cambiar_estado_articulo, name='cambiar_estado_articulo'),
    
    # URLs para artículos estáticos del blog
    path('articulo1/', views.articulo1, name='articulo1'),
    path('articulo2/', views.articulo2, name='articulo2'),
    path('articulo3/', views.articulo3, name='articulo3'),
    path('articulo4/', views.articulo4, name='articulo4'),
    path('articulo5/', views.articulo5, name='articulo5'),
    

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

