from django.core.management.base import BaseCommand
from apppatarescata.models import Usuario

class Command(BaseCommand):
    help = 'Corrige el RUT de una fundación específica que tenga "FUNDACION" como valor temporal'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Email de la fundación a corregir',
        )
        parser.add_argument(
            '--rut',
            type=str,
            help='Nuevo RUT de empresa para la fundación',
        )

    def handle(self, *args, **options):
        email = options['email']
        nuevo_rut = options['rut']
        
        if not email or not nuevo_rut:
            self.stdout.write(
                self.style.ERROR(
                    'Debes proporcionar tanto el email como el nuevo RUT.\n'
                    'Uso: python manage.py corregir_rut_fundacion --email email@ejemplo.com --rut 12345678'
                )
            )
            return
        
        try:
            # Buscar la fundación por email
            fundacion = Usuario.objects.get(email=email, rut_empresa="FUNDACION")
            
            # Validar que el nuevo RUT sea numérico y tenga entre 7 y 9 dígitos
            if not nuevo_rut.isdigit() or len(nuevo_rut) < 7 or len(nuevo_rut) > 9:
                self.stdout.write(
                    self.style.ERROR(
                        f'El RUT "{nuevo_rut}" no es válido. Debe tener entre 7 y 9 dígitos numéricos.'
                    )
                )
                return
            
            # Actualizar el RUT
            fundacion.rut_empresa = nuevo_rut
            fundacion.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'RUT de empresa actualizado exitosamente para {fundacion.nombre}.\n'
                    f'Email: {fundacion.email}\n'
                    f'Nuevo RUT: {fundacion.rut_empresa}'
                )
            )
            
        except Usuario.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    f'No se encontró una fundación con email "{email}" que tenga "FUNDACION" como RUT temporal.'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'Error al actualizar el RUT: {str(e)}'
                )
            )
