from django import forms
from django.shortcuts import render
from django.utils import timezone
from apppatarescata.models import FAQ, ArticuloBlog

from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Usuario
from .models import Mascota
from .models import Numero,rut

from django.core.exceptions import ValidationError




class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['pregunta']
        widgets = {
            'pregunta': forms.Textarea(attrs={'class': 'custom-input'}),
        }



class Formulario2(forms.Form):
    
    regiones = [('RM', 'Region Metropolitana')]

    tipo_mascota = [
        ('', ''),
        ('perro', 'Perro'),
        ('gato', 'Gato'),
    ]

    tamaño_mascota = [
        ('', ''),
        ('miniatura', 'Miniatura'),
        ('pequeño', 'Pequeño'),
        ('mediano', 'Mediano'),
        ('grande', 'Grande'),
        ('gigante', 'Gigante'),
    ]
    comunas_de_santiago = [
        ('', ''),
        ('SANTIAGO', 'Santiago'),
        ('INDEPENDENCIA', 'Independencia'),
        ('ÑUÑOA', 'Ñuñoa'),
        ('MACUL', 'Macul'),
        ('PROVIDENCIA', 'Providencia'),
        ('LAS CONDES', 'Las Condes'),
        ('LA REINA', 'La Reina'),
        ('PEÑALOLÉN', 'Peñalolén'),
        ('SAN JOAQUÍN', 'San Joaquín'),
        ('LA CISTERNA', 'La Cisterna'),
        ('SAN MIGUEL', 'San Miguel'),
        ('PEDRO AGUIRRE CERDA', 'Pedro Aguirre Cerda'),
        ('CERRILLOS', 'Cerrillos'),
        ('ESTACIÓN CENTRAL', 'Estación Central'),
        ('PUDAHUEL', 'Pudahuel'),
        ('MAIPÚ', 'Maipú'),
        ('CERRO NAVIA', 'Cerro Navia'),
        ('LO PRADO', 'Lo Prado'),
        ('QUINTA NORMAL', 'Quinta Normal'),
        ('RENCA', 'Renca'),
        ('HUECHURABA', 'Huechuraba'),
        ('CONCHALÍ', 'Conchalí'),
        ('QUILICURA', 'Quilicura'),
        ('LO BARNECHEA', 'Lo Barnechea'),
        ('VITACURA', 'Vitacura'),
        ('LA FLORIDA', 'La Florida'),
        ('LA GRANJA', 'La Granja'),
        ('LO ESPEJO', 'Lo Espejo'),
        ('RECOLETA', 'Recoleta'),
        ('SAN BERNARDO', 'San Bernardo'),
        ('SAN RAMÓN', 'San Ramón'),
    ]

    opciones_edades = [
        ('', ''),  # Opción por defecto
        ("1M", "1M"),
        ("2M", "2M"),
        ("3M", "3M"),
        ("4M", "4M"),
        ("5M", "5M"),
        ("6M", "6M"),
        ("7M", "7M"),
        ("8M", "8M"),
        ("9M", "9M"),
        ("10M", "10M"),
        ("11M", "11M"),
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6"),
        ("7", "7"),
        ("8", "8"),
        ("9", "9"),
        ("10", "10"),
        ("11", "11"),
        ("12", "12"),
        ("13", "13"),
        ("14", "14"),
        ("15", "15"),
        ("16", "16"),
        ("17", "17"),
        ("18", "18"),
        ("19", "19"),
        ("20", "20"),
    ]

    nombre_mascota = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'style': 'font-family: "Passion One", sans-serif;'})
    )
    edad_mascota = forms.ChoiceField(
        choices=opciones_edades,
        widget=forms.Select(attrs={'style': 'font-family: "Passion One", sans-serif;'})
    )
    tipo_mascota = forms.ChoiceField(
        choices=tipo_mascota,
        widget=forms.Select(attrs={'style': 'font-family: "Passion One", sans-serif;'}),
        required=True
    )
    tamaño_mascota = forms.ChoiceField(
        choices=tamaño_mascota,
        widget=forms.Select(attrs={'style': 'font-family: "Passion One", sans-serif;'})
    )
    comuna_mascota = forms.ChoiceField(
        choices=comunas_de_santiago,
        widget=forms.Select(attrs={'style': 'font-family: "Passion One", sans-serif;'})
    )
    region = forms.ChoiceField(
        choices=regiones,
        widget=forms.Select(attrs={'style': 'font-family: "Passion One", sans-serif;'})
    )
    descripcion = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'style': 'font-family: "Passion One", sans-serif;'})
    )
    imagen = forms.ImageField(required=False)
    
    # Nuevos campos para compatibilidad con preferencias del adoptante
    compatible_departamento = forms.ChoiceField(
        choices=[
            ('', 'Selecciona una opción'),
            ('si', 'Sí, ideal para departamento'),
            ('con_restricciones', 'Sí, con restricciones (balcón necesario)'),
            ('no', 'No, requiere casa con patio'),
        ],
        widget=forms.Select(attrs={'style': 'font-family: "Passion One", sans-serif;'}),
        label='Compatible con departamento'
    )
    
    nivel_energia = forms.ChoiceField(
        choices=[
            ('', 'Selecciona una opción'),
            ('bajo', 'Bajo - Tranquilo y relajado'),
            ('medio', 'Medio - Activo pero moderado'),
            ('alto', 'Alto - Muy activo y enérgico'),
        ],
        widget=forms.Select(attrs={'style': 'font-family: "Passion One", sans-serif;'}),
        label='Nivel de energía'
    )
    
    necesidad_atencion = forms.ChoiceField(
        choices=[
            ('', 'Selecciona una opción'),
            ('baja', 'Baja - Independiente'),
            ('media', 'Media - Necesita compañía moderada'),
            ('alta', 'Alta - Requiere mucha atención'),
        ],
        widget=forms.Select(attrs={'style': 'font-family: "Passion One", sans-serif;'}),
        label='Necesidad de atención'
    )
    
    requisitos_espacio = forms.ChoiceField(
        choices=[
            ('', 'Selecciona una opción'),
            ('poco_espacio', 'Poco espacio - Interior pequeño'),
            ('espacio_moderado', 'Espacio moderado - Interior amplio'),
            ('mucho_espacio', 'Mucho espacio - Requiere patio o jardín'),
        ],
        widget=forms.Select(attrs={'style': 'font-family: "Passion One", sans-serif;'}),
        label='Requisitos de espacio'
    )
    
    tiempo_ejercicio = forms.ChoiceField(
        choices=[
            ('', 'Selecciona una opción'),
            ('poco', 'Poco - 30 minutos o menos'),
            ('moderado', 'Moderado - 1-2 horas'),
            ('mucho', 'Mucho - 2+ horas diarias'),
        ],
        widget=forms.Select(attrs={'style': 'font-family: "Passion One", sans-serif;'}),
        label='Tiempo de ejercicio necesario'
    )
    
    sociabilidad = forms.ChoiceField(
        choices=[
            ('', 'Selecciona una opción'),
            ('independiente', 'Independiente - Prefiere estar solo'),
            ('sociable', 'Sociable - Le gusta la compañía'),
            ('muy_sociable', 'Muy sociable - Necesita interacción constante'),
        ],
        widget=forms.Select(attrs={'style': 'font-family: "Passion One", sans-serif;'}),
        label='Nivel de sociabilidad'
    )



def mi_vista(request):
    
    form2 = Formulario2()

    return render(request, 'mi_template.html', { 'form2': form2})




#Se validan el telefono y el rut las def estan en models . py 

class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField()
    rut_empresa = forms.CharField(max_length=20, required=False, label="RUT de Empresa (opcional)")
    
    # Personalizar mensajes de ayuda para contraseñas en español
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = (
            '• Tu contraseña no puede ser muy similar a tu información personal.<br>'
            '• Tu contraseña debe contener al menos 8 caracteres.<br>'
            '• Tu contraseña no puede ser una contraseña comúnmente utilizada.<br>'
            '• Tu contraseña no puede ser completamente numérica.'
        )
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Confirmar Contraseña"

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        Numero(telefono)
        return telefono

    def clean_rut_empresa(self):
        rut_empresa = self.cleaned_data.get('rut_empresa')
        
        # El RUT de empresa es opcional, pero si se proporciona debe ser válido
        if rut_empresa:
            rut(rut_empresa)
        
        return rut_empresa

    class Meta:
        model = Usuario
        fields = ['rut_empresa', 'nombre', 'telefono', 'email', 'password1', 'password2']


class RegistroFundacionForm(UserCreationForm):
    email = forms.EmailField()
    rut_empresa = forms.CharField(
        max_length=20, 
        required=True, 
        label="RUT de Empresa", 
        help_text="Ingresa el RUT sin puntos, solo números y guión (ej: 19956655-5)",
        widget=forms.TextInput(attrs={'placeholder': '19956655-5'})
    )
    
    # Personalizar mensajes de ayuda para contraseñas en español
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = (
            '• Tu contraseña no puede ser muy similar a tu información personal.<br>'
            '• Tu contraseña debe contener al menos 8 caracteres.<br>'
            '• Tu contraseña no puede ser una contraseña comúnmente utilizada.<br>'
            '• Tu contraseña no puede ser completamente numérica.'
        )
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Confirmar Contraseña"

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        Numero(telefono)
        return telefono

    def clean_rut_empresa(self):
        rut_empresa = self.cleaned_data.get('rut_empresa')
        
        # El RUT de empresa es obligatorio para fundaciones
        if not rut_empresa:
            raise ValidationError('El RUT de empresa es obligatorio para fundaciones.')
        
        # Validar formato: solo números, un guión y dígito verificador
        if not rut_empresa or '-' not in rut_empresa:
            raise ValidationError('El RUT debe tener el formato: 19956655-5 (números, guión y dígito verificador).')
        
        # Separar números del dígito verificador
        partes = rut_empresa.split('-')
        if len(partes) != 2:
            raise ValidationError('El RUT debe tener exactamente un guión separando números del dígito verificador.')
        
        numeros = partes[0]
        digito_verificador = partes[1]
        
        # Validar que la primera parte solo contenga números
        if not numeros.isdigit():
            raise ValidationError('La parte numérica del RUT debe contener solo números.')
        
        # Validar que el dígito verificador sea un solo carácter
        if len(digito_verificador) != 1:
            raise ValidationError('El dígito verificador debe ser un solo carácter.')
        
        # Validar que tenga exactamente 8 dígitos (sin contar el dígito verificador)
        if len(numeros) != 8:
            raise ValidationError('El RUT debe tener exactamente 8 dígitos + guión + dígito verificador (ej: 19956655-5).')
        
        # Retornar el RUT tal como se ingresó (con guión)
        return rut_empresa

    class Meta:
        model = Usuario
        fields = ['rut_empresa', 'nombre', 'telefono', 'email', 'password1', 'password2']
        

from django import forms
from django.core.exceptions import ValidationError
from .models import Usuario

class ActualizarPerfilForm(forms.ModelForm):
    rut_empresa = forms.CharField(
        max_length=20, 
        required=False, 
        label="RUT de Empresa",
        help_text="Ingresa el RUT sin puntos, solo números y guión (ej: 19956655-5). Debe tener exactamente 8 dígitos + guión + dígito verificador.",
        widget=forms.TextInput(attrs={'placeholder': '19956655-5'})
    )
    
    class Meta:
        model = Usuario
        fields = ['email', 'nombre', 'telefono', 'rut_empresa']

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono and (len(telefono) != 9 or not telefono.isdigit()):
            raise ValidationError(('El número de teléfono debe tener exactamente 9 dígitos numéricos.'), code='invalid_phone_number')
        return telefono

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Puedes agregar otras validaciones de correo electrónico según tus requisitos
        return email
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            # Limpiar espacios extra y capitalizar
            nombre = ' '.join(nombre.strip().split())
            if len(nombre) < 2:
                raise ValidationError('El nombre debe tener al menos 2 caracteres.')
        return nombre

    def clean_rut_empresa(self):
        rut_empresa = self.cleaned_data.get('rut_empresa')
        if rut_empresa:
            # Validar formato: solo números, un guión y dígito verificador
            if '-' not in rut_empresa:
                raise ValidationError('El RUT debe tener el formato: 19956655-5 (números, guión y dígito verificador).')
            
            # Separar números del dígito verificador
            partes = rut_empresa.split('-')
            if len(partes) != 2:
                raise ValidationError('El RUT debe tener exactamente un guión separando números del dígito verificador.')
            
            numeros = partes[0]
            digito_verificador = partes[1]
            
            # Validar que la primera parte solo contenga números
            if not numeros.isdigit():
                raise ValidationError('La parte numérica del RUT debe contener solo números.')
            
            # Validar que el dígito verificador sea un solo carácter
            if len(digito_verificador) != 1:
                raise ValidationError('El dígito verificador debe ser un solo carácter.')
            
            # Validar que tenga exactamente 8 dígitos (sin contar el dígito verificador)
            if len(numeros) != 8:
                raise ValidationError('El RUT debe tener exactamente 8 dígitos + guión + dígito verificador (ej: 19956655-5).')
            
            # Retornar el RUT tal como se ingresó (con guión)
            return rut_empresa
        return rut_empresa
    










#     nombre_mascota = forms.CharField(
#         max_length=20,
#         widget=forms.TextInput(attrs={'style': 'font-family: "Passion One", sans-serif;'})
#     )
#     edad_mascota = forms.ChoiceField(
#         choices=opciones_edades,
#         widget=forms.Select(attrs={'style': 'font-family: "Passion One", sans-serif;'})
#     )


class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre_mascota', 'edad_mascota', 'tamaño_mascota', 'comuna_mascota', 'region', 'descripcion', 'imagen']
        widgets = {
            'descripcion': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-textarea',
                'placeholder': 'Describe la personalidad, características especiales, necesidades de cuidado y cualquier información importante sobre esta mascota...'
            }),
        }


# Formulario para Artículos del Blog
class ArticuloBlogForm(forms.ModelForm):
    class Meta:
        model = ArticuloBlog
        fields = ['titulo', 'contenido', 'resumen', 'imagen', 'categoria', 'destacado', 'publicado']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título del artículo...',
                'maxlength': '200'
            }),
            'contenido': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 15,
                'placeholder': 'Escribe el contenido del artículo aquí...'
            }),
            'resumen': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Resumen breve del artículo (máximo 300 caracteres)...',
                'maxlength': '300'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-control'
            }),
            'destacado': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'publicado': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer el campo imagen opcional
        self.fields['imagen'].required = False
        # Establecer fecha de publicación automáticamente si se marca como publicado
        if self.instance and self.instance.pk and self.data.get('publicado'):
            if not self.instance.fecha_publicacion:
                self.instance.fecha_publicacion = timezone.now()


# Formulario para el Asistente Virtual
class AsistenteVirtualForm(forms.Form):
    TIPO_VIVIENDA_CHOICES = [
        ('', 'Selecciona una opción'),
        ('casa', 'Casa'),
        ('departamento', 'Departamento'),
        ('casa_con_patio', 'Casa con patio'),
        ('departamento_pequeño', 'Departamento pequeño'),
    ]
    
    ESPACIOS_DISPONIBLES_CHOICES = [
        ('', 'Selecciona una opción'),
        ('solo_interior', 'Solo interior'),
        ('interior_y_balcon', 'Interior y balcón'),
        ('interior_y_patio_pequeno', 'Interior y patio pequeño'),
        ('interior_y_patio_grande', 'Interior y patio grande'),
        ('mucho_espacio_exterior', 'Mucho espacio exterior'),
    ]
    
    TIEMPO_LIBRE_CHOICES = [
        ('', 'Selecciona una opción'),
        ('poco_tiempo', 'Poco tiempo (1-2 horas/día)'),
        ('tiempo_moderado', 'Tiempo moderado (3-4 horas/día)'),
        ('mucho_tiempo', 'Mucho tiempo (5+ horas/día)'),
        ('solo_fines_semana', 'Solo fines de semana'),
    ]
    
    TAMAÑO_PREFERIDO_CHOICES = [
        ('', 'Selecciona una opción'),
        ('miniatura', 'Miniatura'),
        ('pequeño', 'Pequeño'),
        ('mediano', 'Mediano'),
        ('grande', 'Grande'),
        ('gigante', 'Gigante'),
        ('sin_preferencia', 'Sin preferencia'),
    ]
    
    tipo_vivienda = forms.ChoiceField(
        choices=TIPO_VIVIENDA_CHOICES,
        label="Tipo de vivienda",
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    espacios_disponibles = forms.ChoiceField(
        choices=ESPACIOS_DISPONIBLES_CHOICES,
        label="Espacios disponibles",
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    tiempo_libre = forms.ChoiceField(
        choices=TIEMPO_LIBRE_CHOICES,
        label="Tiempo libre disponible",
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    tamaño_preferido = forms.ChoiceField(
        choices=TAMAÑO_PREFERIDO_CHOICES,
        label="Tamaño preferido",
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        tipo_vivienda = cleaned_data.get('tipo_vivienda')
        espacios_disponibles = cleaned_data.get('espacios_disponibles')
        tiempo_libre = cleaned_data.get('tiempo_libre')
        tamaño_preferido = cleaned_data.get('tamaño_preferido')
        
        # Verificar que al menos un campo esté seleccionado
        if not any([tipo_vivienda, espacios_disponibles, tiempo_libre, tamaño_preferido]):
            raise forms.ValidationError("Por favor selecciona al menos una preferencia para recibir recomendaciones personalizadas.")
        
        return cleaned_data


# Formulario para suscripción al newsletter
class NewsletterSubscriptionForm(forms.Form):
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={
            'class': 'newsletter-input',
            'placeholder': 'Tu correo electrónico',
            'required': True
        })
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Verificar si ya existe una suscripción activa
            from .models import NewsletterSubscription
            if NewsletterSubscription.objects.filter(email=email, activo=True).exists():
                raise forms.ValidationError("Este correo ya está suscrito a nuestro newsletter.")
        return email