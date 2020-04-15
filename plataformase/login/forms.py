# login/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from RVOES.models import Acuerdos


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email', 'curp_rfc', 'calle', 'noexterior',
                  'nointerior', 'codigopostal', 'municipio', 'colonia',
                  'celular', 'tipo_usuario', 'tipo_persona', 'first_name',
                  'last_name', 'departamento')


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('username', 'email', 'curp_rfc', 'calle', 'noexterior',
                  'nointerior', 'codigopostal', 'municipio', 'colonia',
                  'celular', 'tipo_usuario', 'tipo_persona', 'first_name',
                  'last_name', 'departamento')

class AcuerdosForms(forms.ModelForm):
    class Meta:
        model = Acuerdos
        fields = '__all__'

#-------------------------VISITANTE---------------------------
