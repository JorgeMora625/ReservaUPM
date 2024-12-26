from django.test import TestCase
from .models import *

# Models tests--------------------------------------------------------------------------------------------------------------------------
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