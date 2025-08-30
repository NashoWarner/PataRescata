from django.core.management.base import BaseCommand
from apppatarescata.models import Usuario

class Command(BaseCommand):
    help = 'Actualiza las cuentas existentes de fundaciones que tengan "FUNDACION" como valor en rut_empresa'

    def handle(self, *args, **options):
        # Buscar usuarios que tengan "FUNDACION" como rut_empresa
        fundaciones_con_rut_temporal = Usuario.objects.filter(rut_empresa="FUNDACION")
        
        if fundaciones_con_rut_temporal.exists():
            self.stdout.write(
                self.style.WARNING(
                    f'Se encontraron {fundaciones_con_rut_temporal.count()} fundaciones con RUT temporal "FUNDACION"'
                )
            )
            
            for fundacion in fundaciones_con_rut_temporal:
                self.stdout.write(
                    f'Fundación: {fundacion.nombre} (Email: {fundacion.email}) - RUT actual: {fundacion.rut_empresa}'
                )
            
            self.stdout.write(
                self.style.WARNING(
                    '\nEstas fundaciones necesitan actualizar su RUT de empresa real en el perfil.\n'
                    'El valor "FUNDACION" era temporal y no es un RUT válido.\n'
                    'Por favor, pídeles que actualicen su perfil con el RUT real de su empresa.'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    'No se encontraron fundaciones con RUT temporal "FUNDACION". Todas las fundaciones tienen RUTs válidos.'
                )
            )
