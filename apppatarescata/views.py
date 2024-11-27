from django.shortcuts import render, redirect
from apppatarescata.models import FAQ, Mascota, MascotaFundacion, Usuario
from .forms import FAQForm, Formulario2, RegistroUsuarioForm, ActualizarPerfilForm
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




def faq(request):
    preguntas = FAQ.objects.all()
    form = FAQForm()
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/nosotros')

    data = {'preguntas': preguntas, 'form': form}
    return render(request, 'nosotros.html', data)


@login_required(login_url='/login/')
def agregarMascota(request):
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
            fundacion = request.user if request.user.rut_empresa else None
            MascotaFundacion.objects.create(mascota=nueva_mascota, adoptante=fundacion)

            return redirect('/')
    else:
        form2 = Formulario2()

    data = {'mascotas': mascotas, 'form2': form2}
    return render(request, 'nuevamascota.html', data)




def buscar_animales(request):
    animales = []

    if request.method == 'GET':
        tamaño_mascota = request.GET.get('tamaño', '')
        region = request.GET.get('region', '')
        edad_mascota = request.GET.get('edad', '')
        comuna_mascota = request.GET.get('comuna', '')

        animales = Mascota.objects.filter(
            Q(tamaño_mascota__iexact=tamaño_mascota) | Q(tamaño_mascota__icontains=tamaño_mascota),
            Q(region__icontains=region),
            Q(edad_mascota__iexact=edad_mascota) | Q(edad_mascota__icontains=edad_mascota),
            Q(comuna_mascota__iexact=comuna_mascota) | Q(comuna_mascota__icontains=comuna_mascota)
        )
    data = {'animales': animales}
    return render(request, 'index.html', data)



def resultado_busqueda(request):
    animales = []

    if request.method == 'GET':
        tamaño_mascota = request.GET.get('tamaño', '')
        region = request.GET.get('region', '')
        edad_mascota = request.GET.get('edad', '')
        comuna_mascota = request.GET.get('comuna', '')

        animales = Mascota.objects.filter(
            Q(tamaño_mascota__iexact=tamaño_mascota) | Q(tamaño_mascota__icontains=tamaño_mascota),
            Q(region__icontains=region),
            Q(edad_mascota__iexact=edad_mascota) | Q(edad_mascota__icontains=edad_mascota),
            Q(comuna_mascota__iexact=comuna_mascota) | Q(comuna_mascota__icontains=comuna_mascota)
        )

    context = {'animales': animales}
    return render(request, 'resultado_busqueda.html', context)



def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()

            # Generar el enlace de verificación
            token = user.token_verificacion
            dominio = get_current_site(request).domain
            enlace_verificacion = reverse('verificar-cuenta', kwargs={'token': token})
            enlace_absoluto = 'http://'+dominio+enlace_verificacion

            # Enviar el correo electrónico de verificación
            send_mail(
                'Verifica tu cuenta',
                'Haz click en el enlace para verificar tu cuenta: '+enlace_absoluto,
                'jordan4retro142@gmail.com',
                [user.email],
                fail_silently=False,
            )

            user = authenticate(request, email=email, password=password)

            return redirect('mi_login')

    else:
        form = RegistroUsuarioForm()

    return render(request, 'registro_usuario.html', {'form': form})



def mi_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(request, username=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, '¡Inicio de sesión exitoso!')

            return redirect('home_perfil')

        else:
            error_message = 'Email o contraseña incorrectos. Por favor, verifica tus credenciales.'
            messages.add_message(request, messages.ERROR, error_message)

    return render(request, 'miperfil.html')



def logout_view(request):
    logout(request)
    return redirect('/')



@login_required(login_url='/login/')
def info_perfil(request):
    usuario = request.user

    if usuario.is_authenticated:
        nombre = usuario.nombre
        telefono = usuario.telefono
        email = usuario.email
        rut_empresa = usuario.rut_empresa

        data = {'nombre': nombre, 'telefono': telefono, 'email': email, 'rut_empresa': rut_empresa}
        return render(request, 'home_perfil.html', data)
    else:
        return redirect('mi_login')



@login_required(login_url='/login/')
def actualizar_perfil(request):
    usuario = request.user

    if request.method == 'POST':
        form = ActualizarPerfilForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('home_perfil')
    else:
        form = ActualizarPerfilForm(instance=usuario)

    return render(request, 'edicionperfil.html', {'form': form})



@login_required(login_url='/login/')
def eliminar_cuenta(request):
    if request.method == 'POST':
        confirmacion = request.POST.get('confirmacion', '')
        if confirmacion.lower() == 'confirmar':
            request.user.delete()
            logout(request)
            messages.success(request, 'Tu cuenta ha sido eliminada correctamente.')
            return redirect('/')
        else:
            messages.error(request, 'Confirmación incorrecta. La cuenta no ha sido eliminada.')

    return render(request, 'eliminar_cuenta.html')




@login_required(login_url='/login/')
def realizar_adopcion(request, animal_id):
    mascota = Mascota.objects.get(id=animal_id)
    adoptante = request.user
    adopcion_existente = Adopcion.objects.filter(mascota=mascota, adoptante=adoptante)

    if adopcion_existente.exists():
        messages.error(request, 'Ya has solicitado informacion de este animal anteriormente.')
        return redirect('mis_solicitudes')
    adopciones_usuario = Adopcion.objects.filter(adoptante=adoptante)

    if adopciones_usuario.count() >= 3:
        messages.error(request, 'Ya has alcanzado el límite de solicitudes (3 animales).')
        return redirect('mis_solicitudes')
    
    if mascota:
        Adopcion.objects.create(mascota=mascota, adoptante=adoptante)
        mascota.adopcion_solicitada = True
        mascota.save()
        adopciones = Adopcion.objects.filter(adoptante=adoptante)
        context = {'adopciones': adopciones}
        messages.success(request, 'Has solicitado más información! ')
        return render(request, 'solicitudes.html', context)
    else:
        messages.error(request, 'No se pudo realizar la solicitud.')
        return redirect('mis_solicitudes')


@login_required(login_url='/login/')
def mis_solicitudes(request):
    usuario = request.user

    adopciones = Adopcion.objects.filter(adoptante=usuario)

    context = {'adopciones': adopciones}
    return render(request, 'solicitudes.html', context)






def preguntas_frecuentes(request):
    return render(request, 'faq.html')


def home(request):
    return render(request, 'index.html')


def nosotros(request):
    return render(request, 'nosotros.html')


def blog(request):
    return render(request, 'blog.html')


def articulo1(request):
    return render(request, 'articulo1.html')


def articulo2(request):
    return render(request, 'articulo2.html')


def articulo3(request):
    return render(request, 'articulo3.html')


def articulo4(request):
    return render(request, 'articulo4.html')


def articulo5(request):
    return render(request, 'articulo5.html')


def navegador(request):
    return render(request, 'navegador.html')


def home_perfil(request):
    return render(request, 'home_perfil.html')

def solicitudes_perfil(request):
    return render(request, 'solicitudes.html')





def verificar_cuenta(request, token):
    try:
        usuario = Usuario.objects.get(token_verificacion=token)  # Cambia esta línea
        usuario.email_verificado = True
        usuario.save()
        return HttpResponse('Cuenta verificada exitosamente')
    except Usuario.DoesNotExist:  # Cambia esta línea
        return HttpResponse('Token inválido')
    

def tienda(request):
    # Recupera el valor seleccionado en el desplegable
    ordenar_por = request.GET.get('ordenar_por', None)

    # Aplica la lógica de ordenamiento
    if ordenar_por == "precio_asc":
        productos = Producto.objects.all().order_by('precio')
    elif ordenar_por == "precio_desc":
        productos = Producto.objects.all().order_by('-precio')
    else:
        productos = Producto.objects.all()

    return render(request, 'tienda.html', {'productos': productos, 'ordenar_por': ordenar_por})


