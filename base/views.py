from django.http import HttpResponse, JsonResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.conf import settings

from base.decorators import profesor_required
from base.utils import enviar_correo

from .forms import RegistroForm, NuevoLaboratorio, ReservaForm 
from .models import Reserva, Laboratorio

import calendar
import datetime
import time
import threading

from apscheduler.schedulers.background import BackgroundScheduler # type: ignore

# Create your views here.
#-------------------------------------------------------USUARIOS----------------------------------------------------------------------
class MyLogin(LoginView):
    template_name = 'base/inicio_sesion.html'
    field = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('principal')
    
    def form_invalid(self, form):
        messages.error(self.request, 'Usuario o contraseña incorrectos.')
        return super().form_invalid(form)
    


def logout_view(request):
    logout(request)
    return render(request, 'base/logout.html')



def registroUsuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('principal')  
    else:
        form = RegistroForm()
    return render(request, 'base/registro-user.html', {'form': form})



def ver_perfil(request):
    usr_actual = request.user
    if 'alumnos' in usr_actual.email:
        rol = 'Alumno'
    else:
        rol = 'Profesor'
    return render(request, 'base/ver_perfil.html', {'usr': usr_actual, 'rol': rol})

#-------------------------------------------------------LABORATORIOS----------------------------------------------------------------------
@profesor_required
def adminLaboratorios(request):
    if request.method == 'POST':
        form = NuevoLaboratorio(request.POST)
        if form.is_valid():
            form.save()
            return redirect('principal')
    else:
        form = NuevoLaboratorio()
    return render(request, 'base/laboratorio_form.html', {'form':form})



class obtener_laboratorios(LoginRequiredMixin, ListView):
    model = Laboratorio
    context_object_name = 'laboratorios'
    template_name = 'base/laboratorios.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        valor_buscado = self.request.GET.get('barra_busqueda') or ''
        if valor_buscado:
            context['laboratorios'] = context['laboratorios'].filter(cod_lab__icontains=valor_buscado)
        context['valor_buscado'] = valor_buscado
        return context
    
    def get_queryset(self):
        return Laboratorio.objects.all().order_by('bloque')



@login_required
def eliminar_laboratorio(request, id_laboratorio):
    laboratorio = get_object_or_404(Laboratorio, id=id_laboratorio)
    if request.method == 'POST':
        laboratorio.delete()
        return redirect('laboratorios')
    
    return render(request, 'base/eliminar_laboratorio.html', {'laboratorio': laboratorio})



@login_required
def modificar_laboratorio(request, pk):
    laboratorio = get_object_or_404(Laboratorio, pk=pk)
    initial_data = {
        'cod_lab': laboratorio.cod_lab,
        'bloque': laboratorio.bloque,
        'capacidad': laboratorio.capacidad
    }

    if request.method == 'POST':
        form = NuevoLaboratorio(request.POST, instance=laboratorio)
        if form.is_valid():
            form.save()
            return redirect('laboratorios')
        else:
            print(form.errors)
    else:
        form = NuevoLaboratorio(instance=laboratorio)
    return render(request, 'base/modificar_laboratorio.html', {'form': form, 'laboratorio': laboratorio})



@login_required
def ver_laboratorio(request, id_laboratorio):
    laboratorio = get_object_or_404(Laboratorio, id=id_laboratorio)
    return render(request, 'base/ver_laboratorio.html', {'laboratorio': laboratorio})

#-------------------------------------------------------RESERVAS------------------------------------------------------------------------
class Mis_Reservas(LoginRequiredMixin, ListView):
    model = Reserva
    context_object_name = 'reservas'
    template_name = 'base/mis_reservas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reservas'] = context['reservas'].filter(usuario=self.request.user)
        context['hoy'] = datetime.datetime.now().date()
        context['hora_actual'] = datetime.datetime.now().time()
        return context
    
    def get_queryset(self):
        return Reserva.objects.all().order_by('-fecha_reserva')



@login_required
def mostrarBloques(request):
    bloques_unicos = set()
    for obj in Laboratorio.objects.all():
        if obj.bloque not in bloques_unicos:
            bloques_unicos.add(obj.bloque)
    return render(request, 'base/bloques.html', {'bloques': bloques_unicos})



@login_required
def mostrarLaboratorios(request, bloque_seleccionado):
    laboratorios = Laboratorio.objects.filter(bloque=bloque_seleccionado)
    lab = laboratorios[0]
    request.session['bloque_seleccionado'] = bloque_seleccionado
    return render(request, 'base/labs_por_bloque.html', {'laboratorios': laboratorios, 'bloque_seleccionado': bloque_seleccionado, 'lab': lab})



@login_required
def calendario(request, cod_lab):
    lab_seleccionado = get_object_or_404(Laboratorio, cod_lab=cod_lab)
    request.session['laboratorio_seleccionado'] = lab_seleccionado.cod_lab

    today = datetime.date.today()
    current_year = today.year
    current_month = today.month

    cal = calendar.Calendar()
    months = []

    months_traductions = {'January':'Enero', 'February':'Febrero', 'March':'Marzo', 'April':'Abril', 
             'May':'Mayo', 'June':'Junio', 'July':'Julio', 'August':'Agosto', 
             'September':'Septiembre', 'October':'Octubre', 'November':'Noviembre', 'December':'Diciembre'} 
    
    for month in range(current_month, current_month + 3):
        year = current_year + (month - 1) // 12  # Ajustar el año si es necesario
        month = (month - 1) % 12 + 1  # Ajustar el mes para que esté en [1, 12]
        month_days = cal.monthdayscalendar(year, month)

        months.append({
            'year': year,
            'month': month,
            'month_name': months_traductions[calendar.month_name[month]],
            'days': month_days,
        })
    
    bloque = request.session.get('bloque_seleccionado')
    fecha_hoy = datetime.date.today()
    return render(request, 'base/calendario.html', {'months': months, 'bloque': bloque, 'dia_actual': fecha_hoy})



@login_required
def hora_reserva(request, day, month, year):
    request.session['año_seleccionado'] = year
    request.session['mes_seleccionado'] = month
    request.session['dia_seleccionado'] = day

    if request.method == 'POST':
        hora_inicio = request.POST.get('hora_inicio')
        hora_fin = request.POST.get('hora_fin')
        if(hora_fin > hora_inicio):
            request.session['hora_inicio'] = hora_inicio
            request.session['hora_fin'] = hora_fin
        elif(hora_fin <= hora_inicio):
            messages.error(request, 'La hora de fin no puede ser menor o igual que la hora de inicio')
        return redirect('detalles_Reserva')
    
    laboratorio_seleccionado = request.session.get('laboratorio_seleccionado')
    return render(request, 'base/hora_inicio_fin.html', {'laboratorio_seleccionado': laboratorio_seleccionado})


@login_required
def detalles_Reserva(request): 
    hora_inicio = request.session.get('hora_inicio')
    hora_fin = request.session.get('hora_fin')
    bloque_seleccionado = request.session.get('bloque_seleccionado')
    laboratorio_seleccionado = request.session.get('laboratorio_seleccionado')
    dia = request.session.get('dia_seleccionado')
    mes = request.session.get('mes_seleccionado')
    año = request.session.get('año_seleccionado')
    date_selected = datetime.date(año, mes, dia)
    fecha_actual = datetime.date.today()
    return render(request, 'base/detalles_Reserva.html', {'bloque_seleccionado': bloque_seleccionado, 'fecha_actual': fecha_actual, 
        'laboratorio_seleccionado': laboratorio_seleccionado, 'date_selected': date_selected, 'hora_inicio': hora_inicio, 'hora_fin': hora_fin})



def incrementar_capacidad(request, duracion):
    time.sleep(duracion)
    laboratorio_seleccionado = request.session.get('laboratorio_seleccionado')
    lab = Laboratorio.objects.get(cod_lab=laboratorio_seleccionado)
    lab.incrementar()

@login_required
def guardar_Reserva(request):
    if request.method == 'POST':
        año = request.session.get('año_seleccionado')
        mes = request.session.get('mes_seleccionado')
        dia = request.session.get('dia_seleccionado')
        fecha = datetime.date(año, mes, dia)
        hora_inicio = request.session.get('hora_inicio')
        hora_fin = request.session.get('hora_fin')
        cod_lab = request.session.get('laboratorio_seleccionado')
        lab = Laboratorio.objects.get(cod_lab=cod_lab)

        nueva_reserva = Reserva(
            usuario = request.user,
            fecha_reserva = fecha,
            laboratorio = lab,
            hora_inicio = hora_inicio,
            hora_fin = hora_fin
        )
        nueva_reserva.save()

        lab.decrementar()

        cuerpo = f"""Hola {request.user.first_name}, \n\n Te confirmamos que se ha realizado correctamente tu reserva. \n Detalles: 
        Bloque: {nueva_reserva.laboratorio.bloque}
        Laboratorio: {nueva_reserva.laboratorio.cod_lab}
        Fecha: {nueva_reserva.fecha_reserva} 
        Horario: {hora_inicio} - {hora_fin}
        Realizada en: {nueva_reserva.fecha_creacion} 
        \n Puedes cancelar o realizar modificaciones desde la web Reserva UPM."""

        enviar_correo(request.user.email, 'Reserva confirmada.', cuerpo)

        hora = datetime.datetime.strptime(nueva_reserva.hora_fin, "%H:%M").time()
        fecha_hora = datetime.datetime.combine(nueva_reserva.fecha_reserva, hora)
        ahora = datetime.datetime.now()
        tiempo = fecha_hora - ahora
        segundos = int(tiempo.total_seconds())
        print(segundos)
        thread = threading.Thread(target=incrementar_capacidad, args=(request, segundos))
        thread.start()

        return redirect('principal')
    else: 
        return HttpResponse("No se ha podido guardar.")



@login_required
def eliminar_reserva(request, id_reserva):
    reserva = get_object_or_404(Reserva, id=id_reserva)
    if request.method == 'POST':
        reserva.delete()
        reserva.laboratorio.incrementar()
        return redirect('mis_reservas')
    
    return render(request, 'base/eliminar_reserva.html', {'reserva': reserva})



@login_required
def editar_reserva(request, id_reserva):
    reserva = get_object_or_404(Reserva, id=id_reserva)
    initial_data = {
        'bloque': reserva.laboratorio.bloque,
        'laboratorio': reserva.laboratorio.cod_lab,
        'fecha_reserva': reserva.fecha_reserva,
        'hora_inicio' : reserva.hora_inicio,
        'hora_fin' : reserva.hora_fin
    }

    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            fecha_reserva = form.cleaned_data['fecha_reserva']
            bloque = form.cleaned_data['bloque'] 
            laboratorio = form.cleaned_data['laboratorio']
            hora_inicio = form.cleaned_data['hora_inicio']
            hora_fin = form.cleaned_data['hora_fin']
            # Editamos la misma reserva
            reserva = get_object_or_404(Reserva, id=id_reserva)
            reserva.fecha_reserva = fecha_reserva
            reserva.laboratorio = Laboratorio.objects.get(cod_lab=laboratorio)
            reserva.hora_inicio = hora_inicio
            reserva.hora_fin = hora_fin
            reserva.laboratorio.decrementar()
            reserva.save()
            return redirect('mis_reservas')
    else:
        form = ReservaForm(initial=initial_data)
    
    return render(request, 'base/editar_reserva.html', {'reserva': reserva, 'form': form})



@login_required
def ver_reserva(request, id_reserva):
    reserva = get_object_or_404(Reserva, id=id_reserva)
    return render(request, 'base/ver_reserva.html', {'reserva': reserva})

#-------------------------------------------------------OTROS---------------------------------------------------------------------------
@login_required
def principal(request):
    hoy = datetime.date.today()
    hora_actual = datetime.datetime.now().time()
    reservas_mes = Reserva.objects.filter(
        usuario_id=request.user.id, 
        fecha_reserva__year=hoy.year, 
        fecha_reserva__month=hoy.month, 
        fecha_reserva__gte=hoy
    ).order_by('fecha_reserva')
    dia_hoy = hoy.day
    return render(request, 'base/principal.html', {'reservas_mes': reservas_mes, 'hora_actual': hora_actual, 'dia_hoy': dia_hoy})



def inicio(request):
    return render(request, 'base/inicio.html')

