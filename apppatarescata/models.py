from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager 



import secrets

def generar_token():
    return secrets.token_hex(20)

# Definición del modelo Mascota
class Mascota(models.Model):
    nombre_mascota = models.CharField(max_length=20)
    edad_mascota = models.CharField(max_length=5)  
    tamaño_mascota = models.CharField(max_length=50)
    comuna_mascota = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='imagenes_mascotas/', blank=True, null=True)
    adopcion_solicitada = models.BooleanField(default=False)

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

# Definición del modelo Usuario
class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15, validators=[Numero])
    rut_empresa = models.CharField(max_length=20, null=True, blank=True, validators=[rut])
    email_verificado = models.BooleanField(default=False)
    token_verificacion = models.CharField(max_length=40, default=generar_token)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'telefono']

    objects = UserManager()

# Definición del modelo MascotaFundacion
class MascotaFundacion(models.Model):
    id = models.AutoField(primary_key=True)
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    adoptante = models.ForeignKey(Usuario, on_delete=models.CASCADE)

# Definición del modelo Adopcion
class Adopcion(models.Model):
    adoptante = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='adopciones_solicitadas')
    fecha_adopcion = models.DateField(auto_now_add=True)
    solicitada = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.adoptante.nombre} adoptó a {self.mascota.nombre_mascota}"
    




