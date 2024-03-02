from django.test import TestCase
from django.urls import reverse

# Create your tests here.



        

class UrlsTest(TestCase):


    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home2(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_preguntas_frecuentes(self):
        response = self.client.get(reverse('preguntas_frecuentes'))
        self.assertEqual(response.status_code, 200)

    def test_navegador(self):
        response = self.client.get('/navegador/')
        self.assertEqual(response.status_code, 200)

    def test_blog(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

    def test_articulo5(self):
        response = self.client.get('/articulo5/')
        self.assertEqual(response.status_code, 200)

    def test_articulo4(self):
        response = self.client.get('/articulo4/')
        self.assertEqual(response.status_code, 200)

    def test_articulo3(self):
        response = self.client.get('/articulo3/')
        self.assertEqual(response.status_code, 200)

    def test_articulo2(self):
        response = self.client.get('/articulo2/')
        self.assertEqual(response.status_code, 200)

    def test_articulo1(self):
        response = self.client.get('/articulo1/')
        self.assertEqual(response.status_code, 200)

    def test_faq(self):
        response = self.client.get(reverse('faq'))
        self.assertEqual(response.status_code, 200)


from apppatarescata.models import Usuario, Mascota  # Asegúrate de importar tu modelo de Usuario correctamente

class AuthenticationTest(TestCase):
    def setUp(self):
        self.user = Usuario.objects.create_user(
        email='testuser@gmail.com',
        password='Naxito5421',
        nombre='Test User',
        telefono='66694033',
        # Puedes agregar más campos aquí si son necesarios
    )

        self.mascota = Mascota.objects.create(
        nombre_mascota='Test Mascota',
        edad_mascota='1M',
        tamaño_mascota='Mediano',
        comuna_mascota='Quinta Normal',
        region='RM',
        descripcion='Test Descripcion',
        # Puedes agregar más campos aquí si son necesarios
    )

    def test_login(self):
        self.client.login(email='testuser@gmail.com', password='Naxito5421')
        response = self.client.get(reverse('mi_login'))
        self.assertEqual(response.status_code, 200)

    def test_actualizar_perfil(self):
        self.client.login(email='testuser@gmail.com', password='Naxito5421')
        response = self.client.get(reverse('actualizar_perfil'))
        self.assertEqual(response.status_code, 200)


    def test_buscar_animal(self):
        self.client.login(email='testuser@gmail.com', password='Naxito5421')
        self.client.get(reverse('buscar_animales'), {'tamaño_mascota': 'Mediano'})
        response = self.client.get(reverse('resultado_busqueda'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Mascota')

    def test_resultado_busqueda(self):
        self.client.login(email='testuser@gmail.com', password='testuser@gmail.com')
        params = {
            'tamaño_mascota': 'mediano',
        }
        response = self.client.get(reverse('resultado_busqueda'), params)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Mascota')


    def test_mis_solicitudes(self):
        self.client.login(email='testuser@gmail.com', password='Naxito5421')
        response = self.client.get(reverse('mis_solicitudes'))
        self.assertEqual(response.status_code, 200)