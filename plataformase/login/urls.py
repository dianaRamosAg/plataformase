# login/urls.py
from django.urls import path, include
from .views import *
from django.conf.urls import url
from django.views.generic.base import TemplateView
from .views import *

urlpatterns = [
    path('signup/', SignUpView, name='signup'),
    path('', include('django.contrib.auth.urls'), name='login'),
    path('signupr/', regUser, name='signupr'),
    path('root/editar/actualizarusr/', actualizarusr, name='actualizarusr'),
    path('perfil/', perfil, name='perfil'),
    path('docAnexos/', docAnexos, name='docAnexos'),
    path('root/', inicioRoot, name='root'),
    path('root/usuarios', usuarios, name='usuarios'),
    path('root/editar/<email>/',ActUsr, name='editar'),
]
 