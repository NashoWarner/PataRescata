from django.contrib import admin
from django.urls import path
from apppatarescata import views
from apppatarescata.views import estadisticas
from apppatarescata.views import (
    faq, home, blog, nosotros, preguntas_frecuentes, agregarMascota, 
    buscar_animales, resultado_busqueda, mi_login, 
    logout_view, info_perfil, articulo1, articulo2, articulo3, articulo4, 
    articulo5, navegador, home_perfil, actualizar_perfil, actualizar_perfil_adoptante, eliminar_cuenta, 
    realizar_adopcion, mis_solicitudes, verificar_cuenta, tienda, probar_email,
    gestionar_blog, crear_articulo, editar_articulo, eliminar_articulo, 
    cambiar_estado_articulo, ver_articulo, seleccionar_tipo_cuenta, 
    login_adoptante, login_fundacion, registro_adoptante, registro_fundacion,
    perfil_adoptante, generar_solicitud_adopcion, preparar_adopcion,
    aprobar_solicitud_adopcion, rechazar_solicitud_adopcion, cuidado_animal, eventos,
    recuperar_password_adoptante, recuperar_password_fundacion, restablecer_password,
    recuperar_password_universal
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('preguntas-frecuentes/', preguntas_frecuentes, name='preguntas_frecuentes'),
    path('admin/', admin.site.urls),
    path('navegador/', navegador, name='navegador'),
    path('blog/', blog, name='blog'),
    path('articulo5/', articulo5, name='articulo5'),
    path('articulo4/', articulo4, name='articulo4'),
    path('articulo3/', articulo3, name='articulo3'),
    path('articulo2/', articulo2, name='articulo2'),
    path('articulo1/', articulo1, name='articulo1'),
    path('nosotros/', nosotros, name='nosotros'),
    path('faq/', faq, name='faq'),
    path('cuidado-animal/', cuidado_animal, name='cuidado_animal'),
    path('eventos/', eventos, name='eventos'),
    path('realizar_adopcion/<int:animal_id>/', realizar_adopcion, name='realizar_adopcion'),
    path('preparar-adopcion/<int:mascota_id>/', preparar_adopcion, name='preparar_adopcion'),
    path('mis_solicitudes/', mis_solicitudes, name='mis_solicitudes'),
    path('aprobar-solicitud/<int:solicitud_id>/', aprobar_solicitud_adopcion, name='aprobar_solicitud'),
    path('rechazar-solicitud/<int:solicitud_id>/', rechazar_solicitud_adopcion, name='rechazar_solicitud'),
    path('', home, name='home'),
    path('tienda/', tienda, name='tienda'),
    path('home_perfil/', info_perfil, name='home_perfil'), 
    path('perfil-adoptante/', perfil_adoptante, name='perfil_adoptante'),
    path('generar-solicitud-adopcion/<int:mascota_id>/', generar_solicitud_adopcion, name='generar_solicitud_adopcion'),
    path('agregarmascota/', agregarMascota, name='agregarmascota'),
    path('buscar_animales/', buscar_animales, name='buscar_animales'),
    path('resultado_busqueda/', resultado_busqueda, name='resultado_busqueda'),
    path('login/', mi_login, name='mi_login'), 
    path('registro/', registro_adoptante, name='registro_usuario'),
    path('seleccionar-tipo/', seleccionar_tipo_cuenta, name='seleccionar_tipo_cuenta'),
    path('login-adoptante/', login_adoptante, name='login_adoptante'),
    path('login-fundacion/', login_fundacion, name='login_fundacion'),
    path('registro-adoptante/', registro_adoptante, name='registro_adoptante'),
    path('registro-fundacion/', registro_fundacion, name='registro_fundacion'),
    path('logout/', logout_view, name='logout'),
    path('actualizar_perfil/', actualizar_perfil, name='actualizar_perfil'),
    path('actualizar_perfil_adoptante/', actualizar_perfil_adoptante, name='actualizar_perfil_adoptante'),
    path('eliminar-cuenta/', eliminar_cuenta, name='eliminar_cuenta'),
    path('verificar-cuenta/<str:token>/', verificar_cuenta, name='verificar_cuenta'),
    path('listar_mascotas/', views.listar_mascotas, name='listar_mascotas'),
    path('eliminar_mascota/<int:mascota_id>/', views.eliminar_mascota, name='eliminar_mascota'),
    path('eliminar_mascotas/', views.eliminar_mascotas, name='eliminar_mascotas'),
    path('contar_mascotas/', views.contar_mascotas, name='contar_mascotas'),
    path('actualizar_mascota/<int:mascota_id>/', views.actualizar_mascota, name='actualizar_mascota'),
    path('estadisticas/', estadisticas, name='estadisticas'),
    path('probar-email/', probar_email, name='probar_email'),
    path('edicionperfil/', actualizar_perfil, name='edicionperfil'),
    path('solicitudes/', mis_solicitudes, name='solicitudes'),
    path('adopciones/', mis_solicitudes, name='adopciones'),
    path('buscador_mascotas/', buscar_animales, name='buscador_mascotas'),
    
    # URLs para gestión del blog (solo administradores)
    path('gestionar-blog/', gestionar_blog, name='gestionar_blog'),
    path('crear-articulo/', crear_articulo, name='crear_articulo'),
    path('editar-articulo/<int:articulo_id>/', editar_articulo, name='editar_articulo'),
    path('eliminar-articulo/<int:articulo_id>/', eliminar_articulo, name='eliminar_articulo'),
    path('cambiar-estado-articulo/<int:articulo_id>/', cambiar_estado_articulo, name='cambiar_estado_articulo'),
    
    # URLs públicas del blog
    path('blog/<slug:slug>/', ver_articulo, name='ver_articulo'),
    
    # URLs para recuperar contraseñas
    path('recuperar-password-adoptante/', recuperar_password_adoptante, name='recuperar_password_adoptante'),
    path('recuperar-password-fundacion/', recuperar_password_fundacion, name='recuperar_password_fundacion'),
    path('restablecer-password/<str:token>/', restablecer_password, name='restablecer_password'),
    path('recuperar-password/', recuperar_password_universal, name='recuperar_password_universal'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

