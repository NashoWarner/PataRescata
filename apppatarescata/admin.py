from django.contrib import admin

# Register your models here.


from apppatarescata.models import Producto

productos = [
    {
        "nombre": "Alimento Premium para Cachorros",
        "descripcion": "Ideal para el crecimiento saludable de cachorros.",
        "precio": 20000,
        "imagen": "productos/alimento_cachorros.jpg"
    },
    {
        "nombre": "Alimento Senior para Perros",
        "descripcion": "Especialmente formulado para perros mayores de 7 años.",
        "precio": 22000,
        "imagen": "productos/alimento_senior.jpg"
    },
    {
        "nombre": "Alimento Hipoalergénico para Perros",
        "descripcion": "Para perros con alergias alimentarias.",
        "precio": 30000,
        "imagen": "productos/alimento_hipoalergenico.jpg"
    },
    {
        "nombre": "Alimento Light para Perros",
        "descripcion": "Ayuda a mantener un peso saludable en perros adultos.",
        "precio": 18000,
        "imagen": "productos/alimento_light.jpg"
    },
    {
        "nombre": "Alimento Orgánico para Perros",
        "descripcion": "Hecho con ingredientes 100% naturales y orgánicos.",
        "precio": 35000,
        "imagen": "productos/alimento_organico.jpg"
    }
]

for producto in productos:
    # Evita duplicados basándote en el nombre
    if not Producto.objects.filter(nombre=producto["nombre"]).exists():
        Producto.objects.create(
            nombre=producto["nombre"],
            descripcion=producto["descripcion"],
            precio=producto["precio"],
            imagen=producto["imagen"]
        )

print("Productos creados exitosamente.")
