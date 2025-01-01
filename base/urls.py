from django.urls import path
from base import admin
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
        path('', inicio, name='inicio'),
        path('login/', MyLogin.as_view(), name='login'),
        path('logout/', logout_view, name='logout'),
        path('registro-usuarios/', registroUsuario, name='registro'),
        path('mis-reservas/', Mis_Reservas.as_view(), name='mis_reservas'),
        path('principal/', principal, name='principal'),
        path('admin-laboratorios/', adminLaboratorios, name='laboratorio_form'),
        # Funcionan si el usuario ha iniciado sesion
        path('password-change/', auth_views.PasswordChangeView.as_view(template_name='base/password_change_form.html'), name='password_change'),
        path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='base/password_change_done.html'), name='password_change_done'),
        path('bloques/', mostrarBloques, name='bloques'),
        path('bloques/Bloque <str:bloque_seleccionado>/', mostrarLaboratorios, name='bloques-lab'),
        path('calendario/<str:cod_lab>/', calendario, name='calendario'),
        path('hora-reserva/<int:day>/<int:month>/<int:year>/', hora_reserva, name='hora_reserva'),
        path('detalles-reserva/', detalles_Reserva, name='detalles_Reserva'),
        path('guardado/', guardar_Reserva, name='guardar_Reserva'),
        path('eliminar-reserva/<int:id_reserva>/', eliminar_reserva, name='eliminar_reserva'),
        path('detalles-reserva/<int:id_reserva>/', ver_reserva, name='ver_reserva'),
        path('editar-reserva/<int:id_reserva>/', editar_reserva, name='editar_reserva'),
        path('laboratorios-list/', obtener_laboratorios.as_view(), name='laboratorios'),
        path('eliminar-laboratorio/<int:id_laboratorio>/', eliminar_laboratorio, name='eliminar_laboratorio'),
        path('detalles-laboratorio/<int:id_laboratorio>/', ver_laboratorio, name='ver_laboratorio'),
        path('editar-laboratorio/<int:pk>/', modificar_laboratorio, name='editar_laboratorio'),
        path('perfil/', ver_perfil, name='perfil'),
        #Olvidé mi contraseña
        path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
        path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
        path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
        path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    ]