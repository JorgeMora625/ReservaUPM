from django.test import TestCase
from .models import *
from .forms import *
from .views import *
from django.urls import reverse

# MODELS TEST--------------------------------------------------------------------------------------------------------------------------
class AlumnoTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="prueba", first_name="prueba", last_name="de alumno", email="prueba@alumnos.upm.es", password="prueba")

    def test_crea_alumno(self):
        usuario = User.objects.get(last_name="de alumno")
        id_user = usuario.id
        alumno = Alumnos.objects.get(nombre="prueba")
        id_alumno = alumno.id
        self.assertEqual(id_user, id_alumno)


class ProfesorTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="prueba", first_name="prueba", last_name="de profesor", email="prueba@upm.es", password="prueba")

    def test_crea_profesor(self):
        usuario = User.objects.get(last_name="de profesor")
        id_user = usuario.id
        profesor = Profesores.objects.get(nombre="prueba")
        id_profesor = profesor.id
        self.assertEqual(id_user, id_profesor)


# FORMS TESTS----------------------------------------------------------------------------------------------------------------------------
class UsuarioTestCase(TestCase):
    def test_correo_inválido(self):
        data = {'username': 'test', 'first_name': 'test', 'last_name': 'de correo', 'email': 'test@gmail.com', 'password1': 'T35tTes7',
             'password2': 'T35tTes7'}
        form = RegistroForm(data=data)
        self.assertFalse(form.is_valid())

        # Verifica que se haya generado el error en el campo email
        self.assertIn('email', form.errors)

        # Comprueba que el mensaje de error es el creado en el formulario
        self.assertEqual(form.errors['email'][0], "El correo debe pertenecer a la UPM")


class LaboratorioTestCase(TestCase):
    def test_bloque_invalido(self):
        data = {'cod_lab': '3333', 'bloque': '4', 'capacidad': '1'}
        form = NuevoLaboratorio(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('bloque', form.errors)
        self.assertEqual(form.errors['bloque'][0], "El bloque no coincide con el código del laboratorio")


class ReservaTestCase(TestCase):
    def test_fecha_invalida(self):
        data = {'fecha_reserva': '2024-7-30', 'hora_inicio': '10:15', 'hora_fin': '13:15', 'bloque': '1', 'laboratorio': '1302'}
        form = ReservaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('fecha_reserva', form.errors)
        self.assertEqual(form.errors['fecha_reserva'][0], "La fecha no puede ser anterior a hoy.")
    
    def test_hora_fin_invalida(self):
        data2 = {'fecha_reserva': '2024-12-27', 'hora_inicio': '10:15', 'hora_fin': '09:15', 'bloque': '1', 'laboratorio': '1302'}
        form = ReservaForm(data=data2)
        self.assertFalse(form.is_valid())
        self.assertIn('hora_fin', form.errors)
        self.assertEqual(form.errors['hora_fin'][0], "La hora de fin no puede ser anterior a la hora de inicio.")

    def test_bloque_invalido(self):
        data3 = {'fecha_reserva': '2024-12-27', 'hora_inicio': '10:15', 'hora_fin': '11:15', 'bloque': '5', 'laboratorio': '1302'}
        form = ReservaForm(data=data3)
        self.assertFalse(form.is_valid())
        self.assertIn('bloque', form.errors)
        self.assertEqual(form.errors['bloque'][0], "El bloque no existe.")

    def test_laboratorio_invalido(self):
        data3 = {'fecha_reserva': '2024-12-27', 'hora_inicio': '10:15', 'hora_fin': '11:15', 'bloque': '1', 'laboratorio': '1111'}
        form = ReservaForm(data=data3)
        self.assertFalse(form.is_valid())
        self.assertIn('laboratorio', form.errors)
        self.assertEqual(form.errors['laboratorio'][0], "El laboratorio no existe.")


#VIEWS TESTS----------------------------------------------------------------------------------------------------------------------------
class ViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', first_name='test', last_name='test', email='test@upm.es', 
            password='testpassword')
        self.user.save()

    def test_inicio(self):
        response = self.client.get(reverse('inicio'))
        self.assertEqual(response.status_code, 200)

    def test_MyLogin(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
    
    def test_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
    
    def test_registroUsuario(self):
        response = self.client.get(reverse('registro'))
        self.assertEqual(response.status_code, 200)

    def test_ver_perfil(self):
        # Autenticar al usuario
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('perfil'))
        self.assertEqual(response.status_code, 200)

    def test_adminLaboratorios(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('laboratorio_form'))
        self.assertEqual(response.status_code, 200)

    def test_obtenerLaboratorios(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('laboratorios'))
        self.assertEqual(response.status_code, 200)
    
    def test_eliminar_laboratorio(self):
        self.client.login(username='testuser', password='testpassword')
        lab = Laboratorio.objects.create(cod_lab=1111, bloque=1, capacidad=1, capacidad_total=1)
        response = self.client.get(reverse('eliminar_laboratorio', args=[lab.id]))
        self.assertEqual(response.status_code, 200)

    def test_modificar_laboratorio(self):
        self.client.login(username='testuser', password='testpassword')
        lab = Laboratorio.objects.create(cod_lab=1111, bloque=1, capacidad=1, capacidad_total=1)
        response = self.client.get(reverse('editar_laboratorio', args=[lab.id]))
        self.assertEqual(response.status_code, 200)

    def test_ver_laboratorio(self):
        self.client.login(username='testuser', password='testpassword')
        lab = Laboratorio.objects.create(cod_lab=1111, bloque=1, capacidad=1, capacidad_total=1)
        response = self.client.get(reverse('ver_laboratorio', args=[lab.id]))
        self.assertEqual(response.status_code, 200)

    def test_Mis_Reservas(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('mis_reservas'))
        self.assertEqual(response.status_code, 200)

    def test_Mis_Reservas(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('mis_reservas'))
        self.assertEqual(response.status_code, 200)

    def test_mostrarBloques(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('bloques'))
        self.assertEqual(response.status_code, 200)

    def test_mostrarLaboratorios(self):
        self.client.login(username='testuser', password='testpassword')
        lab = Laboratorio.objects.create(cod_lab=1111, bloque=1, capacidad=1, capacidad_total=1)
        response = self.client.get(reverse('bloques-lab', args=[lab.bloque]))
        self.assertEqual(response.status_code, 200)
    
    def test_calendario(self):
        self.client.login(username='testuser', password='testpassword')
        lab = Laboratorio.objects.create(cod_lab=1111, bloque=1, capacidad=1, capacidad_total=1)
        response = self.client.get(reverse('calendario', args=[lab.cod_lab]))
        self.assertEqual(response.status_code, 200)

    def test_hora_reserva(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('hora_reserva', args=[29, 12, 2024]))
        self.assertEqual(response.status_code, 200)

    def test_eliminar_reserva(self):
        self.client.login(username='testuser', password='testpassword')
        lab = Laboratorio.objects.create(cod_lab=1111, bloque=1, capacidad=1, capacidad_total=1)
        reserva = Reserva.objects.create(usuario=self.user, fecha_reserva='2025-01-01', hora_inicio='08:00', hora_fin='10:00', laboratorio=lab, fecha_creacion='01/01/2024')
        response = self.client.get(reverse('eliminar_reserva', args=[reserva.id]))
        self.assertEqual(response.status_code, 200)

    def test_editar_reserva(self):
        self.client.login(username='testuser', password='testpassword')
        lab = Laboratorio.objects.create(cod_lab=1111, bloque=1, capacidad=1, capacidad_total=1)
        reserva = Reserva.objects.create(usuario=self.user, fecha_reserva='2025-01-01', hora_inicio='08:00', hora_fin='10:00', laboratorio=lab, fecha_creacion='01/01/2024')
        response = self.client.get(reverse('editar_reserva', args=[reserva.id]))
        self.assertEqual(response.status_code, 200)

    def test_ver_reserva(self):
        self.client.login(username='testuser', password='testpassword')
        lab = Laboratorio.objects.create(cod_lab=1111, bloque=1, capacidad=1, capacidad_total=1)
        reserva = Reserva.objects.create(usuario=self.user, fecha_reserva='2025-01-01', hora_inicio='08:00', hora_fin='10:00', laboratorio=lab, fecha_creacion='01/01/2024')
        response = self.client.get(reverse('ver_reserva', args=[reserva.id]))
        self.assertEqual(response.status_code, 200)
    
    def test_principal(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('principal'))
        self.assertEqual(response.status_code, 200)

    



    