from django import forms
from django.shortcuts import render
from apppatarescata.models import FAQ

from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Usuario

from .models import Numero,rut

from django.core.exceptions import ValidationError

# class Formulario1(forms.Form):
#     pregunta = forms.CharField()
#     respuesta = forms.CharField(widget=forms.TextInput(attrs={'disabled': 'true'}))


class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['pregunta']
        widgets = {
            'pregunta': forms.Textarea(attrs={'class': 'custom-input'}),
        }



class Formulario2(forms.Form):
    
    regiones = [('RM', 'Region Metropolitana')]

    tamaño_mascota = [
        ('', ''),
        ('miniatura', 'Miniatura'),
        ('pequeno', 'Pequeño'),
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



def mi_vista(request):
    
    form2 = Formulario2()

    return render(request, 'mi_template.html', { 'form2': form2})




#Se validan el telefono y el rut las def estan en models . py 

class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField()
    rut_empresa = forms.CharField(max_length=20, required=False)

    def telefono(self):
        telefono = self.cleaned_data['telefono']
        Numero(telefono)
        return telefono

    def rut_empresa(self):
        rut_empresa = self.cleaned_data['rut_empresa']
        rut(rut_empresa)
        return rut_empresa

    class Meta:
        model = Usuario
        fields = ['rut_empresa', 'nombre', 'telefono', 'email', 'password1', 'password2']
        

from django import forms
from .models import Usuario

class ActualizarPerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['email', 'telefono']

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono and (len(telefono) != 9 or not telefono.isdigit()):
            raise ValidationError(('El número de teléfono debe tener exactamente 9 dígitos numéricos.'), code='invalid_phone_number')
        return telefono

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Puedes agregar otras validaciones de correo electrónico según tus requisitos
        return email









#     nombre_mascota = forms.CharField(
#         max_length=20,
#         widget=forms.TextInput(attrs={'style': 'font-family: "Passion One", sans-serif;'})
#     )
#     edad_mascota = forms.ChoiceField(
#         choices=opciones_edades,
#         widget=forms.Select(attrs={'style': 'font-family: "Passion One", sans-serif;'})
#     )