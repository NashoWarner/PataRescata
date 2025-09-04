from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils.text import slugify 



import secrets

def generar_token():
    return secrets.token_hex(20)

# Definición del modelo Mascota
class Mascota(models.Model):
    # Información básica
    nombre_mascota = models.CharField(max_length=20)
    edad_mascota = models.CharField(max_length=5)  
    tipo_mascota = models.CharField(max_length=50)  # Campo para tipo de mascota (perro, gato, etc.)
    tamaño_mascota = models.CharField(max_length=50)
    comuna_mascota = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='imagenes_mascotas/', blank=True, null=True)
    adopcion_solicitada = models.BooleanField(default=False)
    disponible = models.BooleanField(default=True)  # True = disponible para adopción, False = no disponible
    
    # Campos para compatibilidad con preferencias del adoptante
    # Compatibilidad con vivienda
    COMPATIBLE_DEPARTAMENTO_CHOICES = [
        ('si', 'Sí, ideal para departamento'),
        ('con_restricciones', 'Sí, con restricciones (balcón necesario)'),
        ('no', 'No, requiere casa con patio'),
    ]
    compatible_departamento = models.CharField(
        max_length=20, 
        choices=COMPATIBLE_DEPARTAMENTO_CHOICES,
        default='si',
        verbose_name='Compatible con departamento'
    )
    
    # Nivel de energía
    NIVEL_ENERGIA_CHOICES = [
        ('bajo', 'Bajo - Tranquilo y relajado'),
        ('medio', 'Medio - Activo pero moderado'),
        ('alto', 'Alto - Muy activo y enérgico'),
    ]
    nivel_energia = models.CharField(
        max_length=20,
        choices=NIVEL_ENERGIA_CHOICES,
        default='medio',
        verbose_name='Nivel de energía'
    )
    
    # Necesidad de atención
    NECESIDAD_ATENCION_CHOICES = [
        ('baja', 'Baja - Independiente'),
        ('media', 'Media - Necesita compañía moderada'),
        ('alta', 'Alta - Requiere mucha atención'),
    ]
    necesidad_atencion = models.CharField(
        max_length=20,
        choices=NECESIDAD_ATENCION_CHOICES,
        default='media',
        verbose_name='Necesidad de atención'
    )
    
    # Requisitos de espacio
    REQUISITOS_ESPACIO_CHOICES = [
        ('poco_espacio', 'Poco espacio - Interior pequeño'),
        ('espacio_moderado', 'Espacio moderado - Interior amplio'),
        ('mucho_espacio', 'Mucho espacio - Requiere patio o jardín'),
    ]
    requisitos_espacio = models.CharField(
        max_length=20,
        choices=REQUISITOS_ESPACIO_CHOICES,
        default='espacio_moderado',
        verbose_name='Requisitos de espacio'
    )
    
    # Tiempo de ejercicio diario necesario
    TIEMPO_EJERCICIO_CHOICES = [
        ('poco', 'Poco - 30 minutos o menos'),
        ('moderado', 'Moderado - 1-2 horas'),
        ('mucho', 'Mucho - 2+ horas diarias'),
    ]
    tiempo_ejercicio = models.CharField(
        max_length=20,
        choices=TIEMPO_EJERCICIO_CHOICES,
        default='moderado',
        verbose_name='Tiempo de ejercicio necesario'
    )
    
    # Sociabilidad
    SOCIABILIDAD_CHOICES = [
        ('independiente', 'Independiente - Prefiere estar solo'),
        ('sociable', 'Sociable - Le gusta la compañía'),
        ('muy_sociable', 'Muy sociable - Necesita interacción constante'),
    ]
    sociabilidad = models.CharField(
        max_length=20,
        choices=SOCIABILIDAD_CHOICES,
        default='sociable',
        verbose_name='Nivel de sociabilidad'
    )

# Definición del modelo FAQ
class FAQ(models.Model):
    pregunta = models.CharField(max_length=1000)
    respuesta = models.CharField(max_length=1000)

# Validaciones para el teléfono y el RUT
def Numero(value):
    if len(value) != 9 or not value.isdigit():
        raise ValidationError(
            _('El número de teléfono debe tener exactamente 9 dígitos.'),
            code='invalid_phone_number'
        )

def rut(value):
    if not value.isdigit() or len(value) < 7 or len(value) > 9:
        raise ValidationError(
            _('El RUT debe ser válido.'),
            code='invalid_rut'
        )



from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


# Definición del modelo Usuario
class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15, validators=[Numero])
    rut_empresa = models.CharField(max_length=20, null=True, blank=True)
    email_verificado = models.BooleanField(default=False)
    token_verificacion = models.CharField(max_length=100, default=generar_token)
    date_joined = models.DateTimeField(auto_now_add=True)
    imagen_perfil = models.ImageField(upload_to='imagenes_perfil/', blank=True, null=True, verbose_name='Imagen de Perfil')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'telefono']

    objects = CustomUserManager()

# Definición del modelo MascotaFundacion
class MascotaFundacion(models.Model):
    id = models.AutoField(primary_key=True)
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    adoptante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='mascotas_fundacion')
    
    class Meta:
        unique_together = ('mascota', 'adoptante')  # Evita duplicados
    
    def __str__(self):
        return f"{self.mascota.nombre_mascota} - {self.adoptante.nombre}"

# Definición del modelo Adopcion
class Adopcion(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
        ('cancelada', 'Cancelada'),
    ]
    
    adoptante = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='adopciones_solicitadas')
    fecha_adopcion = models.DateField(auto_now_add=True)
    fecha_solicitud = models.DateField(auto_now_add=True)
    solicitada = models.BooleanField(default=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_resolucion = models.DateField(null=True, blank=True)
    comentario_fundacion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.adoptante.nombre} adoptó a {self.mascota.nombre_mascota}"
    


from django.db import models

class Producto(models.Model):
    CATEGORIAS = [
        ('comida', 'Comida para Perros'),
        ('juguetes', 'Juguetes para Perros'),
    ]

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/')
    enlace = models.URLField(max_length=500, blank=True, null=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='comida')  # Agregar campo de categoría

    def __str__(self):
        return self.nombre


# Modelo para Artículos del Blog
class ArticuloBlog(models.Model):
    CATEGORIAS = [
        ('adopcion', 'Adopción'),
        ('cuidados', 'Cuidados'),
        ('entrenamiento', 'Entrenamiento'),
        ('salud', 'Salud'),
        ('medioambiente', 'Medio Ambiente'),
        ('viajes', 'Viajes con Mascotas'),
    ]

    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    contenido = models.TextField()
    resumen = models.TextField(max_length=300, blank=True)
    imagen = models.ImageField(upload_to='blog/', blank=True, null=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='cuidados')
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_publicacion = models.DateTimeField(blank=True, null=True)
    publicado = models.BooleanField(default=False)
    destacado = models.BooleanField(default=False)
    visitas = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-fecha_publicacion', '-fecha_creacion']
        verbose_name = 'Artículo del Blog'
        verbose_name_plural = 'Artículos del Blog'

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    @property
    def tiempo_lectura(self):
        """Calcula el tiempo estimado de lectura en minutos"""
        palabras = len(self.contenido.split())
        return max(1, round(palabras / 200))  # 200 palabras por minuto

    def incrementar_visitas(self):
        """Incrementa el contador de visitas"""
        self.visitas += 1
        self.save(update_fields=['visitas'])







