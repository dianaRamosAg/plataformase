# login/urls.py
from django.urls import path, include
from .views import *
from django.conf.urls import url
from django.views.generic.base import TemplateView
from .views import *

urlpatterns = [
    path('signup/', SignUpView, name='signup'), #Registrar usuarios en plataforma 'plantilla'
    path('', include('django.contrib.auth.urls'), name='login'),
    path('signupr/', regUser, name='signupr'),  #Función para registrar los usuarios
    path('root/editar/actualizarusr/', actualizarusr, name='actualizarusr'),#Editar permisos de usuario  
    path('perfil/', perfil, name='perfil'), #Visualizar datos del usuario logeado/actualizar datos
    path('docAnexos/', docAnexos, name='docAnexos'),
    path('eliminarAcuerdos/<id>', eliminarAcuerdo, name='eliminarAcuerdo'),
    path('root/', inicioRoot, name='root'),
    path('root/usuarios', usuarios, name='usuarios'),
    path('root/editar/<email>/',ActUsr, name='editar'),
    path('enviarReporte/', reporte, name='enviarReporte'),  #Función para enviar reportes
    
]
 