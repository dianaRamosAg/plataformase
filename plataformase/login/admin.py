# login/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    """Sirve para personalizar el modelo de autenticación de usuarios.

    Parámetros
    -:param UserAdmin: Personaliza el modelo de autenticación de usuarios.

    """
    #Creamos la variable que contiene el formulario de creación de usuarios
    add_form = CustomUserCreationForm
    #Formulario de modificar usuarios
    form = CustomUserChangeForm
    #Modelo personalizado de usuarios
    model = CustomUser
    #Se utilizan para mostrar el modelo de usuario
    list_display = ['email', 'username',]

#Representación de un modelo en la interfaz de administración
admin.site.register(CustomUser, CustomUserAdmin)
