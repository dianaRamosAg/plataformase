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
    path('', include('visitante.urls')),
  
    #panel de django
    path('admin/', admin.site.urls),
    #urls de app de login
    path('', include('login.urls')),
    #urls de app de TBC
    path('TBC/', include('TBC.urls')),
    #urls de app de RVOES
    path('inicio/', include('RVOES.urls')),
    #urls de app de SETyRS
    path('SETyRS/', include('SETyRS.urls')),
    #urls de app de SIG
    path('SigApp/', include('SigApp.urls')),

]

if settings.DEBUG:
    urlpatterns += [] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [] + static(settings.MEDIA_URL)

