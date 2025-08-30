from django.shortcuts import render, redirect
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.contrib.auth import authenticate, logout
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string

from .models import FAQ, Mascota, MascotaFundacion, Usuario, ArticuloBlog, Adopcion, Producto
from .forms import FAQForm, Formulario2, RegistroUsuarioForm, ActualizarPerfilForm, ArticuloBlogForm, MascotaForm

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
        print("POST data:", request.POST)  # Debug
        print("Form is valid:", form2.is_valid())  # Debug
        if form2.is_valid():
            print("Cleaned data:", form2.cleaned_data)  # Debug
            nueva_mascota = Mascota(
                nombre_mascota=form2.cleaned_data['nombre_mascota'],
                edad_mascota=form2.cleaned_data['edad_mascota'],
                tipo_mascota=form2.cleaned_data['tipo_mascota'],
                tamaño_mascota=form2.cleaned_data['tamaño_mascota'],
                comuna_mascota=form2.cleaned_data['comuna_mascota'],
                region=form2.cleaned_data['region'],
                descripcion=form2.cleaned_data['descripcion'],
                imagen=form2.cleaned_data['imagen'],
            )
            print("Mascota object:", nueva_mascota.__dict__)  # Debug
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





def home(request):
    # Obtener mascotas disponibles para adopción (destacadas)
    mascotas_destacadas = Mascota.objects.filter(disponible=True).order_by('-id')[:6]
    
    context = {
        'mascotas_destacadas': mascotas_destacadas,
        'user': request.user,  # Pasar el usuario al contexto para mostrar mensajes personalizados
    }
    return render(request, 'index.html', context)

def blog(request):
    """Vista para la página del blog con artículos estáticos"""
    return render(request, 'blog.html')

def nosotros(request):
    return render(request, 'nosotros.html')

def preguntas_frecuentes(request):
    return render(request, 'faq.html')



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









def eliminar_articulo(request, articulo_id):
    if not request.user.is_superuser:
        messages.error(request, "No tienes permisos para acceder a esta página.")
        return redirect('home')
    
    articulo = get_object_or_404(ArticuloBlog, id=articulo_id)
    articulo.delete()
    messages.success(request, 'Artículo eliminado exitosamente.')
    return redirect('home')

def cambiar_estado_articulo(request, articulo_id):
    if not request.user.is_superuser:
        messages.error(request, "No tienes permisos para acceder a esta página.")
        return redirect('home')
    
    articulo = get_object_or_404(ArticuloBlog, id=articulo_id)
    articulo.publicado = not articulo.publicado
    articulo.save()
    
    estado = "publicado" if articulo.publicado else "oculto"
    messages.success(request, f'Artículo {estado} exitosamente.')
    return redirect('home')

def articulo1(request):
    """Vista para el artículo 1: Viajar en Avión"""
    return render(request, 'articulo1.html')

def articulo2(request):
    """Vista para el artículo 2: Adoptar vs. Comprar"""
    return render(request, 'articulo2.html')

def articulo3(request):
    """Vista para el artículo 3: Entrenar a Tu Perro"""
    return render(request, 'articulo3.html')

def articulo4(request):
    """Vista para el artículo 4: Alimentación Adecuada"""
    return render(request, 'articulo4.html')

def articulo5(request):
    """Vista para el artículo 5: Medio Ambiente"""
    return render(request, 'articulo5.html')

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
        
        # Verificar si ya existe una solicitud para esta mascota y este adoptante
        solicitud_existente = Adopcion.objects.filter(
            adoptante=request.user,
            mascota=mascota
        ).first()
        
        if solicitud_existente:
            messages.info(request, f'Ya tienes una solicitud pendiente para {mascota.nombre_mascota}.')
            return redirect('perfil_adoptante')
        
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
        
        messages.success(request, f'¡Excelente! Has solicitado adoptar a {mascota.nombre_mascota}. La fundación revisará tu solicitud.')
        return redirect('perfil_adoptante')
        
    except Mascota.DoesNotExist:
        messages.error(request, 'La mascota no está disponible para adopción.')
        return redirect('home')

def preparar_adopcion(request, mascota_id):
    try:
        mascota = Mascota.objects.get(id=mascota_id, disponible=True)
        
        # Si el usuario ya está autenticado y es adoptante, procesar la adopción directamente
        if request.user.is_authenticated and not request.user.rut_empresa:
            # Verificar si ya existe una solicitud para esta mascota y este adoptante
            solicitud_existente = Adopcion.objects.filter(
                adoptante=request.user,
                mascota=mascota
            ).first()
            
            if solicitud_existente:
                messages.info(request, f'Ya tienes una solicitud pendiente para {mascota.nombre_mascota}.')
                return redirect('perfil_adoptante')
            
            # Crear solicitud de adopción directamente
            adopcion = Adopcion.objects.create(
                adoptante=request.user,
                mascota=mascota,
                estado='pendiente',
                fecha_solicitud=timezone.now().date()
            )
            
            # Marcar mascota como no disponible
            mascota.disponible = False
            mascota.save()
            
            messages.success(request, f'¡Excelente! Has solicitado adoptar a {mascota.nombre_mascota}. La fundación revisará tu solicitud. Puedes ver el estado de tu solicitud en tu perfil.')
            return redirect('perfil_adoptante')
        
        # Si el usuario no está autenticado, guardar en sesión y redirigir al login
        elif not request.user.is_authenticated:
            request.session['mascota_pendiente_adopcion'] = mascota_id
            messages.info(request, f'Has seleccionado a {mascota.nombre_mascota} para adoptar. Por favor inicia sesión para continuar.')
            return redirect('login_adoptante')
        
        # Si es una fundación, redirigir al perfil de fundación
        else:
            messages.error(request, 'Solo los adoptantes pueden solicitar adopciones.')
            return redirect('home_perfil')
            
    except Mascota.DoesNotExist:
        messages.error(request, 'La mascota no está disponible para adopción.')
        return redirect('home')

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

def eliminar_solicitud_adopcion(request, solicitud_id):
    """Vista para que los adoptantes eliminen sus solicitudes de adopción"""
    if not request.user.is_authenticated:
        return redirect('login_adoptante')
    
    if request.user.rut_empresa:
        return redirect('home_perfil')
    
    try:
        # Obtener la solicitud y verificar que pertenezca al adoptante
        solicitud = get_object_or_404(
            Adopcion, 
            id=solicitud_id,
            adoptante=request.user
        )
        
        # Solo permitir eliminar solicitudes pendientes
        if solicitud.estado != 'pendiente':
            messages.error(request, 'Solo puedes eliminar solicitudes pendientes.')
            return redirect('perfil_adoptante')
        
        # Obtener el nombre de la mascota antes de eliminar
        nombre_mascota = solicitud.mascota.nombre_mascota
        
        # Marcar la mascota como disponible nuevamente
        mascota = solicitud.mascota
        mascota.disponible = True
        mascota.save()
        
        # Eliminar la solicitud
        solicitud.delete()
        
        messages.success(request, f'Solicitud de adopción para {nombre_mascota} eliminada exitosamente.')
        
    except Adopcion.DoesNotExist:
        messages.error(request, 'La solicitud no existe o no tienes permisos para eliminarla.')
    except Exception as e:
        messages.error(request, 'Error al eliminar la solicitud.')
    
    return redirect('perfil_adoptante')



# Funciones duplicadas eliminadas



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







