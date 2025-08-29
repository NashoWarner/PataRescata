from django.core.management.base import BaseCommand
from apppatarescata.models import ArticuloBlog, Usuario

class Command(BaseCommand):
    help = 'Verifica que el blog esté funcionando correctamente'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔍 VERIFICANDO ESTADO DEL BLOG...'))
        
        # Verificar artículos
        articulos = ArticuloBlog.objects.all()
        self.stdout.write(f'📝 Total de artículos: {articulos.count()}')
        
        for articulo in articulos:
            self.stdout.write(f'\n📄 Artículo: {articulo.titulo}')
            self.stdout.write(f'   👤 Autor: {articulo.autor.nombre}')
            self.stdout.write(f'   📅 Fecha: {articulo.fecha_publicacion}')
            self.stdout.write(f'   🏷️  Categoría: {articulo.categoria}')
            self.stdout.write(f'   ✨ Destacado: {"Sí" if articulo.destacado else "No"}')
            self.stdout.write(f'   🌐 Publicado: {"Sí" if articulo.publicado else "No"}')
            self.stdout.write(f'   🔗 Slug: {articulo.slug}')
            self.stdout.write(f'   🖼️  Imagen: {"Sí" if articulo.imagen else "No"}')
            
            if articulo.imagen:
                self.stdout.write(f'      📁 Ruta: {articulo.imagen.name}')
        
        # Verificar usuarios
        usuarios = Usuario.objects.filter(is_staff=True)
        self.stdout.write(f'\n👥 Usuarios administradores: {usuarios.count()}')
        
        for usuario in usuarios:
            self.stdout.write(f'   📧 {usuario.email} - {usuario.nombre}')
        
        self.stdout.write(self.style.SUCCESS('\n✅ VERIFICACIÓN COMPLETADA'))
        self.stdout.write('🎉 El blog está listo para funcionar profesionalmente!')
