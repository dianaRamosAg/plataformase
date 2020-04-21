"""plataformase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('se/', include('visitante.urls')),
   # path('login/', include('login.urls')),
   # path('', include('visitante.urls')),
    #path('visitante/menu', include('visitante.urls')),
    #path('', views.index, name='index'),
    #Para saber que tipo de usuario entro al sistema
    #path('accounts/profile/', TemplateView.as_view(template_name='perfil.html'), name='perfil'),
    #path('accounts/profile/administrador', TemplateView.as_view(template_name='administrador.html'), name='administrador'),
    #panel de django
    path('admin/', admin.site.urls),
    #urls de app de login
    path('', include('login.urls')),
    #urls de app de usuarios
    path('inicio/', include('usuarios.urls')),
    #urls de SigApp
    path('SigApp/',include('SigApp.urls')),

]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
