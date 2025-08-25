from django.contrib import admin
from django.utils import timezone
from apppatarescata.models import Producto, ArticuloBlog

productos = [
    {
        "nombre": "Alimento Premium para Cachorros",
        "descripcion": "Ideal para el crecimiento saludable de cachorros.",
        "precio": 5859,
        "imagen": "productos/alimento_cachorros.jpg",
        "enlace": "https://www.distribuidoralira.cl/product/pedigree-carne-1-5kg/?gad_source=1&gclid=Cj0KCQiAgJa6BhCOARIsAMiL7V_Dxte2cXidHQHfCbA_Pzupvjb2n5KtddOnxKY4GzKeL2TzAqB_DRgaAj5AEALw_wcB",
        "categoria": "comida"
    },
    {
        "nombre": "Alimento Senior para Perros",
        "descripcion": "Especialmente formulado para perros mayores de 7 años.",
        "precio": 29990,
        "imagen": "productos/alimento_senior.jpg",
        "enlace": "https://www.lider.cl/supermercado/product/sku/4620319/dog-chow-alimento-seco-perro-adulto-multi-proteina-carne?channable=050ee76964003436323033313956&gad_source=1&gclid=Cj0KCQiAgJa6BhCOARIsAMiL7V9FT8YqslJqXQ9PJguTd1ztuo_FPkuayd1V_aaHnWbaLCOasi09fbkaAqGaEALw_wcB&gclsrc=aw.ds",
        "categoria": "comida"
    },
    {
        "nombre": "Alimento Hipoalergénico para Perros",
        "descripcion": "Para perros con alergias alimentarias.",
        "precio": 18990,
        "imagen": "productos/alimento_hipoalergenico.jpg",
        "enlace": "https://www.acuenta.cl/p/cachupin-adulto-carne-arroz-15-kg-cachupin-4533115?channable=050d226964003435333331313535&gad_source=1&gclid=Cj0KCQiAgJa6BhCOARIsAMiL7V8r3FSu70VqubZNZmNv_72EfG1qTnhxE6Os4pH7jkknLnLhczCYOnUaAsd7EALw_wcB&gclsrc=aw.ds",
        "categoria": "comida"
    },
    {
        "nombre": "Alimento Light para Perros",
        "descripcion": "Ayuda a mantener un peso saludable en perros adultos.",
        "precio": 36990,
        "imagen": "productos/alimento_light.jpg",
        "enlace": "https://soypet.cl/producto/alimento-para-perros-adultos-razas-grandes-y-medianas-maintenance-criadores/?attribute_pa_formato=22-kg&gad_source=1&gclid=Cj0KCQiAgJa6BhCOARIsAMiL7V8ixYJS19pti9u45BoeE-ACwsszj0gnchHSa6CDBzB3lyVttW5FrvMaAjlDEALw_wcB",
        "categoria": "comida"
    },
    {
        "nombre": "Alimento Orgánico para Perros",
        "descripcion": "Hecho con ingredientes 100% naturales y orgánicos.",
        "precio": 29490,
        "imagen": "productos/alimento_organico.jpg",
        "enlace": "https://petvet.cl/products/purina-excellent-perro-adulto-maintenance-15kg?variant=43156266483873&country=CL&currency=CLP&utm_medium=product_sync&utm_source=google&utm_content=sag_organic&utm_campaign=sag_organic&gad_source=1&gclid=Cj0KCQiAgJa6BhCOARIsAMiL7V8lGEq9FSTPYCuH4bccvNvGf6aCK2uGOzgputcsza3YUi1UuLMG5hIaAmYoEALw_wcB",
        "categoria": "comida"
    }
]

juguetes = [
    {
        "nombre": "Pelota de Goma para Perros",
        "descripcion": "Ideal para horas de diversión y ejercicio.",
        "precio": 10990,
        "imagen": "productos/pelota_goma.jpg",
        "enlace": "https://www.circular.pet/products/pelota-con-sonido?variant=45146200834295&country=CL&currency=CLP&utm_medium=product_sync&utm_source=google&utm_content=sag_organic&utm_campaign=sag_organic&gad_source=1&gclid=CjwKCAiAxqC6BhBcEiwAlXp4563C-0svdmOtIBv60gPTkOTWhy2X2VQusJNCNwJZmappvo31viaEyxoCVF0QAvD_BwE",
        "categoria": "juguetes"
    },
    {
        "nombre": "Cuerda para Morder",
        "descripcion": "Perfecta para mantener los dientes de tu perro saludables.",
        "precio": 2990,
        "imagen": "productos/cuerda_morder.jpg",
        "enlace": "https://www.misterpet.cl/juguete-cuerda-para-perros-18-cm?utm_source=js-google-shopping-app&utm_medium=js-google-shopping-app&variant_id=104670077&gad_source=1&gclid=CjwKCAiAxqC6BhBcEiwAlXp45wpE0k0UJJTRzoQ6pGFv_6yL3Ay3ThR7ZcZhos3B3LUmGo_E4HndahoCAhMQAvD_BwE",
        "categoria": "juguetes"
    },
    {
        "nombre": "Peluches para Perros",
        "descripcion": "Suaves y duraderos, diseñados especialmente para perros.",
        "precio": 27990,
        "imagen": "productos/peluches.jpg",
        "enlace": "https://alegrestiendachile.com/products/quackduck%E2%84%A2-pato-de-peluche-con-sonido-para-perros?variant=42825909796909&country=CL&currency=CLP&utm_medium=product_sync&utm_source=google&utm_content=sag_organic&utm_campaign=sag_organic&gad_source=1&gclid=CjwKCAiAxqC6BhBcEiwAlXp45xJ9m5xTmvP34lNKI2V5wYtQtdK3yDz9mYjZABAWaHjs3A2OCNf3MRoCi_EQAvD_BwE",
        "categoria": "juguetes"
    },
    {
        "nombre": "Juguete Interactivo para Perros",
        "descripcion": "Mantén a tu perro entretenido y estimulado mentalmente.",
        "precio": 23503,
        "imagen": "productos/juguete_interactivo.jpg",
        "enlace": "https://www.clubdeperrosygatos.cl/shop/juguetes-perros-ygatos/juguetes-para-perros/nina-ottosson-dog-puzzle-brick-nivel-2/",
        "categoria": "juguetes"
    },
    {
        "nombre": "Disco Volador para Perros",
        "descripcion": "Perfecto para jugar al aire libre.",
        "precio": 3390,
        "imagen": "productos/disco_volador.jpg",
        "enlace": "https://starimport.cl/product/frisbee-para-perros-juguete-goma-con-diseno-pelota-hexagonal/?attribute_color=Rojo&gad_source=1",
        "categoria": "juguetes"
    }
]
# Crea o actualiza productos y juguetes
for producto in productos + juguetes:
    if not Producto.objects.filter(nombre=producto["nombre"]).exists():
        Producto.objects.create(
            nombre=producto["nombre"],
            descripcion=producto["descripcion"],
            precio=producto["precio"],
            imagen=producto["imagen"],
            enlace=producto["enlace"],
            categoria=producto["categoria"]
        )
    else:
        prod = Producto.objects.get(nombre=producto["nombre"])
        prod.descripcion = producto["descripcion"]
        prod.precio = producto["precio"]
        prod.imagen = producto["imagen"]
        prod.enlace = producto["enlace"]
        prod.categoria = producto["categoria"]
        prod.save()

print("Productos y juguetes creados o actualizados exitosamente.")


# Configuración del Admin para Artículos del Blog
@admin.register(ArticuloBlog)
class ArticuloBlogAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'categoria', 'autor', 'fecha_creacion', 'publicado', 'destacado', 'visitas']
    list_filter = ['categoria', 'publicado', 'destacado', 'fecha_creacion', 'fecha_publicacion']
    search_fields = ['titulo', 'contenido', 'resumen']
    list_editable = ['publicado', 'destacado']
    readonly_fields = ['fecha_creacion', 'visitas', 'slug']
    prepopulated_fields = {'slug': ('titulo',)}
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo', 'slug', 'categoria', 'autor')
        }),
        ('Contenido', {
            'fields': ('resumen', 'contenido', 'imagen')
        }),
        ('Publicación', {
            'fields': ('publicado', 'destacado', 'fecha_publicacion')
        }),
        ('Estadísticas', {
            'fields': ('fecha_creacion', 'visitas'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es un nuevo artículo
            obj.autor = request.user
        if form.cleaned_data['publicado'] and not obj.fecha_publicacion:
            obj.fecha_publicacion = timezone.now()
        super().save_model(request, obj, form, change)
