import datetime
from urllib import request
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms
from django.contrib import messages
from .models import Laboratorio
from django.contrib.auth import authenticate
    

class RegistroForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, label="Nombre de usuario", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Nombre de usuario',
        'id': 'username'
    }))
    first_name = forms.CharField(max_length=30, required=True, label="Nombre", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Nombre',
        'id': 'first_name'
    }))
    last_name = forms.CharField(max_length=50, required=True, label="Apellidos", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Apellidos',
        'id': 'last_name'
    }))
    email = forms.EmailField(max_length=254, required=True, label="Corero electrónico", widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Correo de la UPM',
        'id': 'email'
    }))
    password1 = forms.CharField(required=True, label="Contraseña", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Contraseña',
        'id': 'password1'
    }))
    password2 = forms.CharField(required=True, label="Confirmar contraseña", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirmar contraseña',
        'id': 'password2'
    }))

    class Meta:
         model = User
         fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_correo(self):
        email = self.cleaned_data['email']
        if not 'upm.es' in email:
            raise ValidationError('El correo debe pertencer a la UPM')
        return email

    def save(self, commit=True):
         user = super(RegistroForm, self).save(commit=False)
         user.username = self.cleaned_data['username']
         user.first_name = self.cleaned_data['first_name']
         user.last_name = self.cleaned_data['last_name']
         user.email = self.clean_correo()  
         if commit:
            user.save()
         return user



class NuevoLaboratorio(forms.ModelForm):
    cod_lab = forms.CharField(label='Código Laboratorio', widget=forms.TextInput(attrs={
        'class': 'etiqueta_campo'
    }))
    bloque = forms.CharField(label='Bloque', widget=forms.TextInput(attrs={
        'class': 'etiqueta_campo'
    }))
    capacidad = forms.IntegerField(label='Capacidad', widget=forms.NumberInput(attrs={
        'class': 'etiqueta_campo'
    }))

    class Meta:
         model = Laboratorio
         fields = ('cod_lab', 'bloque', 'capacidad')
    
    def clean_bloque(self):
        bloque = self.cleaned_data['bloque']
        laboratorio = self.cleaned_data['cod_lab']
        bloque_real = laboratorio[0]
        if bloque != 'CIC':
            if bloque != bloque_real:
                raise ValidationError('El bloque no coincide con el código del laboratorio')
        return bloque



class ReservaForm(forms.Form):
    fecha_reserva = forms.DateField(label='Fecha', widget=forms.DateInput(attrs={
        'id': 'fecha_reserva',
        'placeholder': 'fecha de la reserva',
        'class': 'form-control'
    }))
    hora_inicio = forms.TimeField(label='Hora inicio', widget=forms.TimeInput(attrs={
        'id': 'hora_inicio',
        'placeholder': 'hora de inicio',
        'class': 'form-control'
    }))
    hora_fin = forms.TimeField(label='Hora fin', widget=forms.TimeInput(attrs={
        'id': 'hora_fin',
        'placeholder': 'hora de fin',
        'class': 'form-control'
    }))
    bloque = forms.CharField(label='Laboratorio', widget=forms.TextInput(attrs={
        'id': 'bloque', 
        'placeholder': 'bloque del laboratorio',
        'class': 'form-control'
    }))
    laboratorio = forms.CharField(label='Laboratorio', widget=forms.TextInput(attrs={
        'id': 'laboratorio', 
        'placeholder': 'numero del laboratorio',
        'class': 'form-control'
    }))

    def clean_fecha_reserva(self):
        fecha_reserva = self.cleaned_data['fecha_reserva']
        if fecha_reserva < datetime.date.today(): 
            raise ValidationError('La fecha no puede ser anterior a hoy.')
        return fecha_reserva
    
    def clean_hora_fin(self):
        hora_inicio = self.cleaned_data['hora_inicio']
        hora_fin = self.cleaned_data['hora_fin']
        if hora_fin < hora_inicio:
            raise ValidationError('La hora de fin no puede ser anterior a la hora de inicio.')
        return hora_fin
        
    def clean_bloque(self):
        bloque = self.cleaned_data['bloque']
        if not Laboratorio.objects.filter(bloque=bloque).exists():
            raise ValidationError('El bloque no existe.')
        return bloque
        
    def clean_laboratorio(self):
        laboratorio = self.cleaned_data['laboratorio']
        if not Laboratorio.objects.filter(cod_lab=laboratorio).exists():
            raise ValidationError('El laboratorio no existe.')
        return laboratorio

    

# NO SE USA
'''class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", max_length=254)

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(username=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Email o contraseña incorrectos.")
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data'''

# NO SE USA
'''class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Correo de la UPM',
        'id': 'username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Contraseña',
        'id': 'password'
    }))'''