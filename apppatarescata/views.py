from django.shortcuts import render, redirect
from django.utils import timezone
from apppatarescata.models import FAQ, Mascota, MascotaFundacion, Usuario, ArticuloBlog
from .forms import FAQForm, Formulario2, RegistroUsuarioForm, ActualizarPerfilForm, ArticuloBlogForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.contrib.auth import authenticate, logout
from .models import MascotaFundacion, Mascota, Mascota, Adopcion
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from .models import Producto
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .forms import MascotaForm
from django.db.models import Count
from django import forms
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string

def faq(request):
    preguntas = FAQ.objects.all()
    form = FAQForm()
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tu pregunta ha sido enviada exitosamente.")
            return redirect('faq')

    data = {'preguntas': preguntas, 'form': form}
    return render(request, 'faq.html', data)

@login_required(login_url='/login-fundacion/')
def agregarMascota(request):
    # Verificación EXTRA de seguridad
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login_fundacion')
    
    # Verificar que el usuario sea una fundación
    if not request.user.rut_empresa:
        messages.error(request, "Solo las fundaciones pueden agregar mascotas.")
        return redirect('home_perfil')
    
    mascotas = Mascota.objects.all()

    if request.method == 'POST':
        form2 = Formulario2(request.POST, request.FILES)
        if form2.is_valid():
            nueva_mascota = Mascota(
                nombre_mascota=form2.cleaned_data['nombre_mascota'],
                edad_mascota=form2.cleaned_data['edad_mascota'],
                tamaño_mascota=form2.cleaned_data['tamaño_mascota'],
                comuna_mascota=form2.cleaned_data['comuna_mascota'],
                region=form2.cleaned_data['region'],
                descripcion=form2.cleaned_data['descripcion'],
                imagen=form2.cleaned_data['imagen'],
            )
            nueva_mascota.save()

            # Obtén la fundación actualmente autenticada y asigna la mascota a esa fundación
            fundacion = request.user
            MascotaFundacion.objects.create(mascota=nueva_mascota, adoptante=fundacion)

            messages.success(request, f"La mascota '{nueva_mascota.nombre_mascota}' ha sido agregada exitosamente.")
            return redirect('listar_mascotas')
    else:
        form2 = Formulario2()

    data = {'mascotas': mascotas, 'form2': form2}
    return render(request, 'nuevamascota.html', data)

def cuidado_animal(request):
    """Vista para la página de cuidado animal"""
    return render(request, 'cuidado_animal.html')

def eventos(request):
    """Vista para la página de eventos"""
    return render(request, 'eventos.html')

def buscar_animales(request):
    # Si el usuario está autenticado y es adoptante, redirigir a su perfil
    if request.user.is_authenticated and not request.user.rut_empresa:
        return redirect('perfil_adoptante')
    
    animales = []

    if request.method == 'GET':
        tamaño_mascota = request.GET.get('tamaño', '')
        region = request.GET.get('region', '')
        edad_mascota = request.GET.get('edad', '')
        
        # Filtrar mascotas disponibles
        mascotas = Mascota.objects.filter(disponible=True)
        
        if tamaño_mascota:
            mascotas = mascotas.filter(tamaño_mascota=tamaño_mascota)
        if region:
            mascotas = mascotas.filter(region=region)
        if edad_mascota:
            mascotas = mascotas.filter(edad_mascota=edad_mascota)
        
        # Obtener solo las primeras 6 mascotas para mostrar
        animales = mascotas[:6]

    return render(request, 'buscar_animales.html', {'animales': animales})

def resultado_busqueda(request):
    tamaño_mascota = request.GET.get('tamaño', '')
    region = request.GET.get('region', '')
    edad_mascota = request.GET.get('edad', '')
    
    # Filtrar mascotas disponibles
    mascotas = Mascota.objects.filter(disponible=True)
    
    if tamaño_mascota:
        mascotas = mascotas.filter(tamaño_mascota=tamaño_mascota)
    if region:
        mascotas = mascotas.filter(region=region)
    if edad_mascota:
        mascotas = mascotas.filter(edad_mascota=edad_mascota)
    
    return render(request, 'resultado_busqueda.html', {'mascotas': mascotas})

def home(request):
    # Obtener mascotas disponibles para adopción (destacadas)
    mascotas_destacadas = Mascota.objects.filter(disponible=True).order_by('-id')[:6]
    
    context = {
        'mascotas_destacadas': mascotas_destacadas,
    }
    return render(request, 'index.html', context)

def blog(request):
    articulos = ArticuloBlog.objects.filter(publicado=True).order_by('-fecha_publicacion')
    return render(request, 'blog.html', {'articulos': articulos})

def nosotros(request):
    return render(request, 'nosotros.html')

def preguntas_frecuentes(request):
    return render(request, 'faq.html')

def navegador(request):
    return render(request, 'navegador.html')

def home_perfil(request):
    if not request.user.is_authenticated:
        return redirect('login_fundacion')
    
    # Obtener mascotas de la fundación
    mascotas = Mascota.objects.filter(mascotafundacion__adoptante=request.user)
    
    # Contar mascotas por estado
    total_mascotas = mascotas.count()
    mascotas_disponibles = mascotas.filter(disponible=True).count()
    mascotas_adoptadas = mascotas.filter(disponible=False).count()
    
    # Obtener solicitudes de adopción de la fundación
    solicitudes = Adopcion.objects.filter(
        mascota__mascotafundacion__adoptante=request.user
    )
    total_solicitudes = solicitudes.count()
    
    context = {
        'total_mascotas': total_mascotas,
        'mascotas_disponibles': mascotas_disponibles,
        'mascotas_adoptadas': mascotas_adoptadas,
        'total_solicitudes': total_solicitudes,
        'mascotas': mascotas[:5],  # Solo mostrar las primeras 5
        'usuario': request.user,  # Agregar el usuario al contexto
        
        # Variables para el template
        'nombre': request.user.nombre,
        'telefono': request.user.telefono,
        'email': request.user.email,
        'rut_empresa': request.user.rut_empresa,
        'mascotas_count': total_mascotas,
        'adopciones_count': total_solicitudes,
        
        # Agregar variables adicionales que el template necesita
        'mascotas_count': total_mascotas,
        'adopciones_count': total_solicitudes,
    }
    
    return render(request, 'home_perfil.html', context)

def actualizar_perfil(request):
    if request.method == 'POST':
        form = ActualizarPerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('home_perfil')
    else:
        form = ActualizarPerfilForm(instance=request.user)
    
    return render(request, 'actualizar_perfil.html', {'form': form})

def actualizar_perfil_adoptante(request):
    if request.method == 'POST':
        form = ActualizarPerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('perfil_adoptante')
    else:
        form = ActualizarPerfilForm(instance=request.user)
    
    return render(request, 'actualizar_perfil_adoptante.html', {'form': form})

def eliminar_cuenta(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, 'Tu cuenta ha sido eliminada exitosamente.')
        return redirect('home')
    
    return render(request, 'eliminar_cuenta.html')

def realizar_adopcion(request, animal_id):
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para adoptar.")
        return redirect('login_adoptante')
    
    if request.user.rut_empresa:
        messages.error(request, "Solo los adoptantes pueden realizar adopciones.")
        return redirect('home_perfil')
    
    try:
        mascota = Mascota.objects.get(id=animal_id, disponible=True)
        
        # Crear solicitud de adopción
        adopcion = Adopcion.objects.create(
            adoptante=request.user,
            mascota=mascota,
            estado='pendiente',
            fecha_solicitud=timezone.now().date()
        )
        
        # Marcar mascota como no disponible
        mascota.disponible = False
        mascota.save()
        
        messages.success(request, f'Has solicitado adoptar a {mascota.nombre_mascota}. La fundación revisará tu solicitud.')
        return redirect('perfil_adoptante')
        
    except Mascota.DoesNotExist:
        messages.error(request, 'La mascota no está disponible para adopción.')
        return redirect('buscar_animales')

def mis_solicitudes(request):
    if not request.user.is_authenticated:
        return redirect('login_fundacion')
    
    if request.user.rut_empresa:
        # Es una fundación, mostrar solicitudes de sus mascotas
        solicitudes = Adopcion.objects.filter(
            mascota__mascotafundacion__adoptante=request.user
        ).select_related('adoptante', 'mascota').order_by('-fecha_adopcion')
    else:
        # Es un adoptante, mostrar sus solicitudes
        solicitudes = Adopcion.objects.filter(
            adoptante=request.user
        ).select_related('mascota').order_by('-fecha_adopcion')
    
    return render(request, 'mis_solicitudes.html', {'solicitudes': solicitudes})

def verificar_cuenta(request, token):
    try:
        user = Usuario.objects.get(token_verificacion=token)
        user.email_verificado = True
        # Generar un nuevo token en lugar de establecer None
        user.token_verificacion = get_random_string(length=64)
        user.save()
        messages.success(request, '¡Tu cuenta ha sido verificada exitosamente! Ahora puedes iniciar sesión.')
    except Usuario.DoesNotExist:
        messages.error(request, 'El enlace de verificación no es válido.')
    
    return redirect('seleccionar_tipo_cuenta')

def tienda(request):
    productos = Producto.objects.all()
    return render(request, 'Tienda.html', {'productos': productos})

def probar_email(request):
    try:
        send_mail(
            'Prueba de Email - PataRescata',
            'Este es un email de prueba para verificar que la configuración funciona correctamente.',
            'jordan4retro142@gmail.com',
            ['test@example.com'],
            fail_silently=False,
        )
        return HttpResponse('Email enviado exitosamente')
    except Exception as e:
        return HttpResponse(f'Error al enviar email: {e}')

def gestionar_blog(request):
    if not request.user.is_superuser:
        messages.error(request, "No tienes permisos para acceder a esta página.")
        return redirect('home')
    
    articulos = ArticuloBlog.objects.all().order_by('-fecha_publicacion')
    return render(request, 'gestionar_blog.html', {'articulos': articulos})

def crear_articulo(request):
    if not request.user.is_superuser:
        messages.error(request, "No tienes permisos para acceder a esta página.")
        return redirect('home')
    
    if request.method == 'POST':
        form = ArticuloBlogForm(request.POST, request.FILES)
        if form.is_valid():
            articulo = form.save(commit=False)
            articulo.autor = request.user
            articulo.save()
            messages.success(request, 'Artículo creado exitosamente.')
            return redirect('gestionar_blog')
    else:
        form = ArticuloBlogForm()
    
    return render(request, 'crear_articulo.html', {'form': form})

def editar_articulo(request, articulo_id):
    if not request.user.is_superuser:
        messages.error(request, "No tienes permisos para acceder a esta página.")
        return redirect('home')
    
    articulo = get_object_or_404(ArticuloBlog, id=articulo_id)
    
    if request.method == 'POST':
        form = ArticuloBlogForm(request.POST, request.FILES, instance=articulo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Artículo actualizado exitosamente.')
            return redirect('gestionar_blog')
    else:
        form = ArticuloBlogForm(instance=articulo)
    
    return render(request, 'editar_articulo.html', {'form': form, 'articulo': articulo})

def eliminar_articulo(request, articulo_id):
    if not request.user.is_superuser:
        messages.error(request, "No tienes permisos para acceder a esta página.")
        return redirect('home')
    
    articulo = get_object_or_404(ArticuloBlog, id=articulo_id)
    articulo.delete()
    messages.success(request, 'Artículo eliminado exitosamente.')
    return redirect('gestionar_blog')

def cambiar_estado_articulo(request, articulo_id):
    if not request.user.is_superuser:
        messages.error(request, "No tienes permisos para acceder a esta página.")
        return redirect('home')
    
    articulo = get_object_or_404(ArticuloBlog, id=articulo_id)
    articulo.publicado = not articulo.publicado
    articulo.save()
    
    estado = "publicado" if articulo.publicado else "oculto"
    messages.success(request, f'Artículo {estado} exitosamente.')
    return redirect('gestionar_blog')

def ver_articulo(request, slug):
    try:
        articulo = ArticuloBlog.objects.get(slug=slug, publicado=True)
        
        # Obtener artículos relacionados (mismo autor o categoría)
        articulos_relacionados = ArticuloBlog.objects.filter(
            publicado=True
        ).exclude(id=articulo.id)[:3]
        
        return render(request, 'ver_articulo.html', {
            'articulo': articulo,
            'articulos_relacionados': articulos_relacionados,
        })
    except ArticuloBlog.DoesNotExist:
        messages.error(request, "El artículo no existe o no está publicado.")
        return redirect('blog')

def seleccionar_tipo_cuenta(request):
    return render(request, 'seleccionar_tipo_cuenta.html')

def login_adoptante(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(request, username=email, password=password)

        if user is not None and not user.rut_empresa:  # Solo adoptantes
            auth.login(request, user)
            messages.success(request, '¡Inicio de sesión exitoso como adoptante!')
            
            # Verificar si hay una mascota pendiente de adopción en la sesión
            mascota_id = request.session.get('mascota_pendiente_adopcion')
            if mascota_id:
                # Limpiar la sesión
                del request.session['mascota_pendiente_adopcion']
                # Redirigir a generar la solicitud
                return redirect('generar_solicitud_adopcion', mascota_id=mascota_id)
            
            return redirect('perfil_adoptante')
        else:
            if user and user.rut_empresa:
                messages.error(request, 'Esta cuenta es de fundación. Usa el login de fundaciones.')
            else:
                messages.error(request, 'Email o contraseña incorrectos.')
            return redirect('login_adoptante')

    return render(request, 'login_adoptante.html')

def login_fundacion(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(request, username=email, password=password)

        if user is not None and user.rut_empresa:  # Solo fundaciones
            auth.login(request, user)
            messages.success(request, '¡Inicio de sesión exitoso como fundación!')
            return redirect('home_perfil')
        else:
            if user and not user.rut_empresa:
                messages.error(request, 'Esta cuenta es de adoptante. Usa el login de adoptantes.')
            else:
                messages.error(request, 'Email o contraseña incorrectos.')
            return redirect('login_fundacion')

    return render(request, 'login_fundacion.html')

def registro_adoptante(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            
            # Forzar tipo adoptante
            user.rut_empresa = None
            
            user.set_password(password)
            user.save()

            # Generar el enlace de verificación
            token = user.token_verificacion
            enlace_absoluto = f'http://127.0.0.1:8000/verificar-cuenta/{token}/'

            try:
                send_mail(
                    'Verifica tu cuenta de adoptante',
                    'Haz click en el enlace para verificar tu cuenta: '+enlace_absoluto,
                    'jordan4retro142@gmail.com',
                    [user.email],
                    fail_silently=False,
                )
                messages.success(request, '¡Cuenta de adoptante creada exitosamente! Se ha enviado un email de verificación.')
            except Exception as e:
                messages.warning(request, 'Cuenta creada exitosamente, pero hubo un problema enviando el email de verificación.')

            # Redirigir al login para que inicie sesión
            messages.success(request, '¡Cuenta de adoptante creada exitosamente! Se ha enviado un email de verificación. Ahora puedes iniciar sesión.')
            return redirect('login_adoptante')

    else:
        form = RegistroUsuarioForm()

    return render(request, 'registro_adoptante.html', {'form': form})

def registro_fundacion(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            
            # Forzar tipo fundación
            user.rut_empresa = "FUNDACION"  # Valor temporal para identificar fundaciones
            
            user.set_password(password)
            user.save()

            # Generar el enlace de verificación
            token = user.token_verificacion
            enlace_absoluto = f'http://127.0.0.1:8000/verificar-cuenta/{token}/'

            try:
                send_mail(
                    'Verifica tu cuenta de fundación',
                    'Haz click en el enlace para verificar tu cuenta: '+enlace_absoluto,
                    'jordan4retro142@gmail.com',
                    [user.email],
                    fail_silently=False,
                )
                messages.success(request, '¡Cuenta de fundación creada exitosamente! Se ha enviado un email de verificación.')
            except Exception as e:
                messages.warning(request, 'Cuenta creada exitosamente, pero hubo un problema enviando el email de verificación.')

            # Redirigir al login para que inicie sesión
            messages.success(request, '¡Cuenta de fundación creada exitosamente! Se ha enviado un email de verificación. Ahora puedes iniciar sesión.')
            return redirect('login_fundacion')

    else:
        form = RegistroUsuarioForm()

    return render(request, 'registro_fundacion.html', {'form': form})

def perfil_adoptante(request):
    if not request.user.is_authenticated:
        return redirect('login_adoptante')
    
    if request.user.rut_empresa:
        return redirect('home_perfil')
    
    # Obtener solicitudes de adopción del adoptante
    solicitudes = Adopcion.objects.filter(adoptante=request.user).select_related('mascota')
    
    # Calcular estadísticas en tiempo real
    total_solicitudes = solicitudes.count()
    solicitudes_pendientes = solicitudes.filter(estado='pendiente').count()
    solicitudes_aprobadas = solicitudes.filter(estado='aprobada').count()
    solicitudes_rechazadas = solicitudes.filter(estado='rechazada').count()
    
    context = {
        'solicitudes': solicitudes,
        'total_solicitudes': total_solicitudes,
        'solicitudes_pendientes': solicitudes_pendientes,
        'solicitudes_aprobadas': solicitudes_aprobadas,
        'solicitudes_rechazadas': solicitudes_rechazadas,
        
        # Variables para el template (nombres correctos)
        'solicitudes_count': total_solicitudes,
        'mascotas_adoptadas_count': solicitudes_aprobadas,
        
        # Agregar datos del usuario para el template
        'usuario': request.user,
        'nombre': request.user.nombre,
        'email': request.user.email,
        'telefono': request.user.telefono,
    }
    
    return render(request, 'perfil_adoptante.html', context)

def generar_solicitud_adopcion(request, mascota_id):
    if not request.user.is_authenticated:
        return redirect('login_adoptante')
    
    if request.user.rut_empresa:
        return redirect('home_perfil')
    
    try:
        mascota = Mascota.objects.get(id=mascota_id, disponible=True)
        
        # Crear solicitud de adopción
        adopcion = Adopcion.objects.create(
            adoptante=request.user,
            mascota=mascota,
            estado='pendiente',
            fecha_solicitud=timezone.now().date()
        )
        
        # Marcar mascota como no disponible
        mascota.disponible = False
        mascota.save()
        
        messages.success(request, f'Has solicitado adoptar a {mascota.nombre_mascota}. La fundación revisará tu solicitud.')
        return redirect('perfil_adoptante')
        
    except Mascota.DoesNotExist:
        messages.error(request, 'La mascota no está disponible para adopción.')
        return redirect('buscar_animales')

def preparar_adopcion(request, mascota_id):
    if not request.user.is_authenticated:
        return redirect('login_adoptante')
    
    if request.user.rut_empresa:
        return redirect('home_perfil')
    
    try:
        mascota = Mascota.objects.get(id=mascota_id, disponible=True)
        # Guardar en sesión para usar después del login
        request.session['mascota_pendiente_adopcion'] = mascota_id
        return redirect('login_adoptante')
    except Mascota.DoesNotExist:
        messages.error(request, 'La mascota no está disponible para adopción.')
        return redirect('buscar_animales')

def listar_mascotas(request):
    if not request.user.is_authenticated:
        return redirect('login_fundacion')
    
    if not request.user.rut_empresa:
        return redirect('perfil_adoptante')
    
    mascotas = Mascota.objects.filter(mascotafundacion__adoptante=request.user)
    return render(request, 'listar_mascotas.html', {'mascotas': mascotas})

def eliminar_mascota(request, mascota_id):
    if not request.user.is_authenticated:
        return redirect('login_fundacion')
    
    if not request.user.rut_empresa:
        return redirect('perfil_adoptante')
    
    try:
        mascota = Mascota.objects.get(id=mascota_id, mascotafundacion__adoptante=request.user)
        mascota.delete()
        messages.success(request, 'Mascota eliminada exitosamente.')
    except Mascota.DoesNotExist:
        messages.error(request, 'La mascota no existe o no tienes permisos para eliminarla.')
    
    return redirect('listar_mascotas')

def eliminar_mascotas(request):
    if not request.user.is_authenticated:
        return redirect('login_fundacion')
    
    if not request.user.rut_empresa:
        return redirect('perfil_adoptante')
    
    if request.method == 'POST':
        mascota_ids = request.POST.getlist('mascotas')
        if mascota_ids:
            Mascota.objects.filter(
                id__in=mascota_ids,
                mascotafundacion__adoptante=request.user
            ).delete()
            messages.success(request, f'{len(mascota_ids)} mascota(s) eliminada(s) exitosamente.')
    
    return redirect('listar_mascotas')

def contar_mascotas(request):
    if not request.user.is_authenticated:
        return redirect('login_fundacion')
    
    if not request.user.rut_empresa:
        return redirect('perfil_adoptante')
    
    total_mascotas = Mascota.objects.filter(mascotafundacion__adoptante=request.user).count()
    mascotas_disponibles = Mascota.objects.filter(
        mascotafundacion__adoptante=request.user,
        disponible=True
    ).count()
    
    return render(request, 'contar_mascotas.html', {
        'total_mascotas': total_mascotas,
        'mascotas_disponibles': mascotas_disponibles
    })

def actualizar_mascota(request, mascota_id):
    if not request.user.is_authenticated:
        return redirect('login_fundacion')
    
    if not request.user.rut_empresa:
        return redirect('perfil_adoptante')
    
    try:
        mascota = Mascota.objects.get(id=mascota_id, mascotafundacion__adoptante=request.user)
    except Mascota.DoesNotExist:
        messages.error(request, 'La mascota no existe o no tienes permisos para editarla.')
        return redirect('listar_mascotas')
    
    if request.method == 'POST':
        form = MascotaForm(request.POST, request.FILES, instance=mascota)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mascota actualizada exitosamente.')
            return redirect('listar_mascotas')
    else:
        form = MascotaForm(instance=mascota)
    
    return render(request, 'actualizar_mascota.html', {'form': form, 'mascota': mascota})

def estadisticas(request):
    if not request.user.is_authenticated:
        return redirect('login_fundacion')
    
    if not request.user.rut_empresa:
        return redirect('perfil_adoptante')
    
    # Estadísticas de mascotas de la fundación
    mascotas = Mascota.objects.filter(mascotafundacion__adoptante=request.user)
    total_mascotas = mascotas.count()
    mascotas_disponibles = mascotas.filter(disponible=True).count()
    mascotas_adoptadas = mascotas.filter(disponible=False).count()
    
    # Estadísticas de solicitudes
    solicitudes = Adopcion.objects.filter(mascota__mascotafundacion__adoptante=request.user)
    total_solicitudes = solicitudes.count()
    solicitudes_pendientes = solicitudes.filter(estado='pendiente').count()
    solicitudes_aprobadas = solicitudes.filter(estado='aprobada').count()
    solicitudes_rechazadas = solicitudes.filter(estado='rechazada').count()
    
    # Calcular tasa de éxito
    tasa_exito = 0
    if total_solicitudes > 0:
        tasa_exito = round((solicitudes_aprobadas / total_solicitudes) * 100)
    
    # Estadísticas generales del sistema (para mostrar en el template)
    total_adopciones = Adopcion.objects.filter(estado='aprobada').count()
    total_fundaciones = Usuario.objects.filter(rut_empresa__isnull=False).count()
    total_adoptantes = Usuario.objects.filter(rut_empresa__isnull=True).count()
    
    # Promedio de adopciones por mes (simplificado)
    promedio_adopciones_mes = round(total_adopciones / 12) if total_adopciones > 0 else 0
    
    context = {
        # Estadísticas de la fundación
        'total_mascotas': total_mascotas,
        'mascotas_disponibles': mascotas_disponibles,
        'mascotas_adoptadas': mascotas_adoptadas,
        'total_solicitudes': total_solicitudes,
        'solicitudes_pendientes': solicitudes_pendientes,
        'solicitudes_aprobadas': solicitudes_aprobadas,
        'solicitudes_rechazadas': solicitudes_rechazadas,
        
        # Estadísticas generales del sistema
        'total_adopciones': total_adopciones,
        'total_fundaciones': total_fundaciones,
        'total_adoptantes': total_adoptantes,
        'tasa_exito': tasa_exito,
        'promedio_adopciones_mes': promedio_adopciones_mes,
        
        # Variables específicas para fundaciones
        'mascotas_fundacion': total_mascotas,
        'adopciones_fundacion': solicitudes_aprobadas,
    }
    
    return render(request, 'estadisticas.html', context)

def mi_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            auth.login(request, user)
            if user.rut_empresa:
                return redirect('home_perfil')
            else:
                return redirect('perfil_adoptante')
        else:
            messages.error(request, 'Email o contraseña incorrectos.')
    
    return render(request, 'login_adoptante.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('home')

def info_perfil(request):
    if not request.user.is_authenticated:
        return redirect('login_fundacion')
    
    # Obtener mascotas de la fundación
    mascotas = Mascota.objects.filter(mascotafundacion__adoptante=request.user)
    
    # Contar mascotas por estado
    total_mascotas = mascotas.count()
    mascotas_disponibles = mascotas.filter(disponible=True).count()
    mascotas_adoptadas = mascotas.filter(disponible=False).count()
    
    # Obtener solicitudes de adopción de la fundación
    solicitudes = Adopcion.objects.filter(
        mascota__mascotafundacion__adoptante=request.user
    )
    total_solicitudes = solicitudes.count()
    
    context = {
        'total_mascotas': total_mascotas,
        'mascotas_disponibles': mascotas_disponibles,
        'mascotas_adoptadas': mascotas_adoptadas,
        'total_solicitudes': total_solicitudes,
        'mascotas': mascotas[:5],  # Solo mostrar las primeras 5
        'usuario': request.user,  # Agregar el usuario al contexto
        
        # Variables para el template
        'nombre': request.user.nombre,
        'telefono': request.user.telefono,
        'email': request.user.email,
        'rut_empresa': request.user.rut_empresa,
        'mascotas_count': total_mascotas,
        'adopciones_count': total_solicitudes,
    }
    
    return render(request, 'home_perfil.html', context)

@login_required(login_url='/login-fundacion/')
def aprobar_solicitud_adopcion(request, solicitud_id):
    """Vista para aprobar una solicitud de adopción"""
    if not request.user.rut_empresa:
        messages.error(request, "Solo las fundaciones pueden aprobar solicitudes.")
        return redirect('home_perfil')
    
    try:
        # Obtener la solicitud y verificar que pertenezca a una mascota de la fundación
        solicitud = get_object_or_404(
            Adopcion, 
            id=solicitud_id,
            mascota__mascotafundacion__adoptante=request.user
        )
        
        # Debug: imprimir estado antes del cambio
        print(f"DEBUG: Estado ANTES de aprobar: {solicitud.estado}")
        
        # Actualizar el estado
        solicitud.estado = 'aprobada'
        solicitud.fecha_resolucion = timezone.now().date()
        
        # Debug: imprimir estado después del cambio
        print(f"DEBUG: Estado DESPUÉS de cambiar: {solicitud.estado}")
        
        # Guardar y verificar
        solicitud.save()
        
        # Debug: verificar si se guardó correctamente
        solicitud.refresh_from_db()
        print(f"DEBUG: Estado DESPUÉS de guardar: {solicitud.estado}")
        
        # Actualizar la mascota para que no aparezca más como disponible
        mascota = solicitud.mascota
        mascota.adopcion_solicitada = True
        mascota.disponible = False  # Marcar como no disponible para adopción
        mascota.save()
        
        messages.success(request, f'Solicitud de adopción para {solicitud.mascota.nombre_mascota} aprobada exitosamente.')
        
    except Adopcion.DoesNotExist:
        messages.error(request, 'La solicitud no existe o no tienes permisos para aprobarla.')
    except Exception as e:
        messages.error(request, 'Error al aprobar la solicitud.')
    
    return redirect('mis_solicitudes')

@login_required(login_url='/login-fundacion/')
def rechazar_solicitud_adopcion(request, solicitud_id):
    """Vista para rechazar una solicitud de adopción"""
    if not request.user.rut_empresa:
        messages.error(request, "Solo las fundaciones pueden rechazar solicitudes.")
        return redirect('home_perfil')
    
    try:
        # Obtener la solicitud y verificar que pertenezca a una mascota de la fundación
        solicitud = get_object_or_404(
            Adopcion, 
            id=solicitud_id,
            mascota__mascotafundacion__adoptante=request.user
        )
        
        # Debug: imprimir estado antes del cambio
        print(f"DEBUG: Estado ANTES de rechazar: {solicitud.estado}")
        
        # Actualizar el estado
        solicitud.estado = 'rechazada'
        solicitud.fecha_resolucion = timezone.now().date()
        
        # Debug: imprimir estado después del cambio
        print(f"DEBUG: Estado DESPUÉS de cambiar: {solicitud.estado}")
        
        # Guardar y verificar
        solicitud.save()
        
        # Debug: verificar si se guardó correctamente
        solicitud.refresh_from_db()
        print(f"DEBUG: Estado DESPUÉS de guardar: {solicitud.estado}")
        
        # Si se rechaza, marcar la mascota como disponible nuevamente
        mascota = solicitud.mascota
        mascota.disponible = True  # Marcar como disponible para adopción
        mascota.save()
        
        messages.success(request, f'Solicitud de adopción para {solicitud.mascota.nombre_mascota} rechazada.')
        
    except Adopcion.DoesNotExist:
        messages.error(request, 'La solicitud no existe o no tienes permisos para rechazarla.')
    except Exception as e:
        messages.error(request, 'Error al rechazar la solicitud.')
    
    return redirect('mis_solicitudes')

def recuperar_password_adoptante(request):
    """Vista para que los adoptantes recuperen su contraseña"""
    if request.method == 'POST':
        email = request.POST.get('email')
        
        if not email:
            messages.error(request, 'Por favor, ingresa un correo electrónico.')
            return render(request, 'recuperar_password_adoptante.html')
        
        try:
            # Buscar usuario por email (solo adoptantes)
            user = Usuario.objects.get(email=email, rut_empresa__isnull=True)
            
            # Generar token único para restablecer contraseña
            token = get_random_string(length=64)
            user.token_verificacion = token
            user.save()
            
            # Crear enlace para restablecer contraseña
            reset_url = f'http://127.0.0.1:8000/restablecer-password/{token}/'
            
            # Enviar email con instrucciones
            try:
                send_mail(
                    'Recuperar Contraseña - PataRescata',
                    f'''Hola {user.nombre},
                    
Has solicitado restablecer tu contraseña. Haz clic en el siguiente enlace para crear una nueva contraseña:

{reset_url}

Este enlace expirará en 24 horas.

Si no solicitaste este cambio, puedes ignorar este email.

Saludos,
El equipo de PataRescata''',
                    'jordan4retro142@gmail.com',
                    [user.email],
                    fail_silently=False,
                )
                messages.success(request, 'Se han enviado las instrucciones a tu correo electrónico.')
            except Exception as e:
                print(f"Error al enviar email: {e}")  # Debug
                messages.error(request, 'Error al enviar el email. Por favor, intenta nuevamente.')
                
        except Usuario.DoesNotExist:
            # No mostrar si el email existe o no por seguridad
            messages.success(request, 'Si el email existe en nuestra base de datos, recibirás las instrucciones.')
        except Exception as e:
            print(f"Error inesperado en recuperar_password_adoptante: {e}")  # Debug
            messages.error(request, 'Error inesperado. Por favor, intenta nuevamente.')
    
    return render(request, 'recuperar_password_adoptante.html')

def recuperar_password_fundacion(request):
    """Vista para que las fundaciones recuperen su contraseña"""
    if request.method == 'POST':
        email = request.POST.get('email')
        
        if not email:
            messages.error(request, 'Por favor, ingresa un correo electrónico.')
            return render(request, 'recuperar_password_fundacion.html')
        
        try:
            # Buscar usuario por email (solo fundaciones)
            user = Usuario.objects.get(email=email, rut_empresa__isnull=False)
            
            # Generar token único para restablecer contraseña
            token = get_random_string(length=64)
            user.token_verificacion = token
            user.save()
            
            # Crear enlace para restablecer contraseña
            reset_url = f'http://127.0.0.1:8000/restablecer-password/{token}/'
            
            # Enviar email con instrucciones
            try:
                send_mail(
                    'Recuperar Contraseña - PataRescata',
                    f'''Hola {user.nombre},
                    
Has solicitado restablecer la contraseña de tu fundación. Haz clic en el siguiente enlace para crear una nueva contraseña:

{reset_url}

Este enlace expirará en 24 horas.

Si no solicitaste este cambio, puedes ignorar este email.

Saludos,
El equipo de PataRescata''',
                    'jordan4retro142@gmail.com',
                    [user.email],
                    fail_silently=False,
                )
                messages.success(request, 'Se han enviado las instrucciones a tu correo electrónico.')
            except Exception as e:
                print(f"Error al enviar email: {e}")  # Debug
                messages.error(request, 'Error al enviar el email. Por favor, intenta nuevamente.')
                
        except Usuario.DoesNotExist:
            # No mostrar si el email existe o no por seguridad
            messages.success(request, 'Si el email existe en nuestra base de datos, recibirás las instrucciones.')
        except Exception as e:
            print(f"Error inesperado en recuperar_password_fundacion: {e}")  # Debug
            messages.error(request, 'Error inesperado. Por favor, intenta nuevamente.')
    
    return render(request, 'recuperar_password_fundacion.html')

def restablecer_password(request, token):
    """Vista para restablecer la contraseña usando el token"""
    try:
        # Buscar usuario por token
        user = Usuario.objects.get(token_verificacion=token)
        
        if request.method == 'POST':
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')
            
            # Validar que las contraseñas coincidan
            if new_password1 != new_password2:
                messages.error(request, 'Las contraseñas no coinciden.')
                return render(request, 'restablecer_password.html')
            
            # Validar que la contraseña cumpla los requisitos mínimos
            if len(new_password1) < 8:
                messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
                return render(request, 'restablecer_password.html')
            
            # Cambiar la contraseña
            user.set_password(new_password1)
            # Generar un nuevo token en lugar de establecer None
            user.token_verificacion = get_random_string(length=64)
            user.save()
            
            messages.success(request, 'Tu contraseña ha sido cambiada exitosamente. Ahora puedes iniciar sesión.')
            return redirect('seleccionar_tipo_cuenta')
        
        return render(request, 'restablecer_password.html')
        
    except Usuario.DoesNotExist:
        messages.error(request, 'El enlace de restablecimiento de contraseña no es válido o ha expirado.')
        return redirect('seleccionar_tipo_cuenta')
    except Exception as e:
        messages.error(request, 'Error inesperado. Por favor, intenta nuevamente.')
        return redirect('seleccionar_tipo_cuenta')

def articulo1(request):
    """Vista para el artículo 1"""
    return render(request, 'articulo1.html')

def articulo2(request):
    """Vista para el artículo 2"""
    return render(request, 'articulo2.html')

def articulo3(request):
    """Vista para el artículo 3"""
    return render(request, 'articulo3.html')

def articulo4(request):
    """Vista para el artículo 4"""
    return render(request, 'articulo4.html')

def articulo5(request):
    """Vista para el artículo 5"""
    return render(request, 'articulo5.html')

def recuperar_password_universal(request):
    """Vista universal para recuperar contraseñas (funciona para adoptantes y fundaciones)"""
    if request.method == 'POST':
        email = request.POST.get('email')
        
        if not email:
            messages.error(request, 'Por favor, ingresa un correo electrónico.')
            return render(request, 'recuperar_password_universal.html')
        
        try:
            # Buscar usuario por email (sin importar el tipo)
            user = Usuario.objects.get(email=email)
            
            # Generar token único para restablecer contraseña
            token = get_random_string(length=64)
            user.token_verificacion = token
            user.save()
            
            # Crear enlace para restablecer contraseña
            reset_url = f'http://127.0.0.1:8000/restablecer-password/{token}/'
            
            # Determinar el tipo de usuario para el mensaje
            tipo_usuario = "fundación" if user.rut_empresa else "adoptante"
            
            # Enviar email con instrucciones
            try:
                send_mail(
                    'Recuperar Contraseña - PataRescata',
                    f'''Hola {user.nombre},
                    
Has solicitado restablecer la contraseña de tu cuenta de {tipo_usuario}. Haz clic en el siguiente enlace para crear una nueva contraseña:

{reset_url}

Este enlace expirará en 24 horas.

Si no solicitaste este cambio, puedes ignorar este email.

Saludos,
El equipo de PataRescata''',
                    'jordan4retro142@gmail.com',
                    [user.email],
                    fail_silently=False,
                )
                messages.success(request, 'Se han enviado las instrucciones a tu correo electrónico.')
                print(f"Email enviado exitosamente a {user.email}")  # Debug
            except Exception as e:
                print(f"Error al enviar email: {e}")  # Debug
                messages.error(request, f'Error al enviar el email: {str(e)}. Por favor, intenta nuevamente.')
                
        except Usuario.DoesNotExist:
            print(f"Usuario no encontrado con email: {email}")  # Debug
            # Por seguridad, no revelar si el email existe o no
            messages.success(request, 'Si el email existe en nuestra base de datos, recibirás las instrucciones.')
        except Exception as e:
            print(f"Error inesperado en recuperar_password_universal: {e}")  # Debug
            messages.error(request, f'Error inesperado: {str(e)}. Por favor, intenta nuevamente.')
    
    return render(request, 'recuperar_password_universal.html')
