from django.contrib import admin
from apppatarescata.models import Producto

productos = [
    {
        "nombre": "Alimento Premium para Cachorros",
        "descripcion": "Ideal para el crecimiento saludable de cachorros.",
        "precio": 5859,
        "imagen": "productos/alimento_cachorros.jpg",
        "enlace": "https://www.distribuidoralira.cl/product/pedigree-carne-1-5kg/?gad_source=1&gclid=Cj0KCQiAgJa6BhCOARIsAMiL7V_Dxte2cXidHQHfCbA_Pzupvjb2n5KtddOnxKY4GzKeL2TzAqB_DRgaAj5AEALw_wcB"
    },
    {
        "nombre": "Alimento Senior para Perros",
        "descripcion": "Especialmente formulado para perros mayores de 7 años.",
        "precio": 29990,
        "imagen": "productos/alimento_senior.jpg",
        "enlace": "https://www.lider.cl/supermercado/product/sku/4620319/dog-chow-alimento-seco-perro-adulto-multi-proteina-carne?channable=050ee76964003436323033313956&gad_source=1&gclid=Cj0KCQiAgJa6BhCOARIsAMiL7V9FT8YqslJqXQ9PJguTd1ztuo_FPkuayd1V_aaHnWbaLCOasi09fbkaAqGaEALw_wcB&gclsrc=aw.ds"
    },
    {
        "nombre": "Alimento Hipoalergénico para Perros",
        "descripcion": "Para perros con alergias alimentarias.",
        "precio": 18990,
        "imagen": "productos/alimento_hipoalergenico.jpg",
        "enlace": "https://www.acuenta.cl/p/cachupin-adulto-carne-arroz-15-kg-cachupin-4533115?channable=050d226964003435333331313535&gad_source=1&gclid=Cj0KCQiAgJa6BhCOARIsAMiL7V8r3FSu70VqubZNZmNv_72EfG1qTnhxE6Os4pH7jkknLnLhczCYOnUaAsd7EALw_wcB&gclsrc=aw.ds"
    },
    {
        "nombre": "Alimento Light para Perros",
        "descripcion": "Ayuda a mantener un peso saludable en perros adultos.",
        "precio": 36990,
        "imagen": "productos/alimento_light.jpg",
        "enlace": "https://soypet.cl/producto/alimento-para-perros-adultos-razas-grandes-y-medianas-maintenance-criadores/?attribute_pa_formato=22-kg&gad_source=1&gclid=Cj0KCQiAgJa6BhCOARIsAMiL7V8ixYJS19pti9u45BoeE-ACwsszj0gnchHSa6CDBzB3lyVttW5FrvMaAjlDEALw_wcB"
    },
    {
        "nombre": "Alimento Orgánico para Perros",
        "descripcion": "Hecho con ingredientes 100% naturales y orgánicos.",
        "precio": 29490,
        "imagen": "productos/alimento_organico.jpg",
        "enlace": "https://petvet.cl/products/purina-excellent-perro-adulto-maintenance-15kg?variant=43156266483873&country=CL&currency=CLP&utm_medium=product_sync&utm_source=google&utm_content=sag_organic&utm_campaign=sag_organic&gad_source=1&gclid=Cj0KCQiAgJa6BhCOARIsAMiL7V8lGEq9FSTPYCuH4bccvNvGf6aCK2uGOzgputcsza3YUi1UuLMG5hIaAmYoEALw_wcB"
    }
]

for producto in productos:
    # Evita duplicados basándote en el nombre
    if not Producto.objects.filter(nombre=producto["nombre"]).exists():
        Producto.objects.create(
            nombre=producto["nombre"],
            descripcion=producto["descripcion"],
            precio=producto["precio"],
            imagen=producto["imagen"],
            enlace=producto["enlace"]
        )
    else:
        # Si el producto ya existe, actualiza su enlace y otros detalles si es necesario
        prod = Producto.objects.get(nombre=producto["nombre"])
        prod.descripcion = producto["descripcion"]
        prod.precio = producto["precio"]
        prod.imagen = producto["imagen"]
        prod.enlace = producto["enlace"]
        prod.save()

print("Productos creados o actualizados exitosamente.")
