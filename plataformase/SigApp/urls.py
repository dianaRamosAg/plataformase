from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name ='SigApp'
#SigMovilFiltros/MEDIA-SUPERIOR/empty/PRIVADA/empty/
urlpatterns = [
    path('',views.index, name='index'),
    path('SigApp/',views.index, name='index'),
    #path('instituciones',views.instituciones, name='instituciones'), 
    path('SigApp/instituciones/<id>/<slug:clave>',views.instituciones, name='instituciones'),   
    path('SigApp/localizador',views.localizador, name='localizador'), 
    path('SigApp/SigMovilFiltros/<slug:mediasuperior>/<slug:superior>/<slug:privada>/<slug:publica>/',views.APIappFiltros,name="filtros"),
    path('SigApp/updl/<int:mun>',views.selecccion_municipio, name='selectMun'),
    path('SigApp/updInstituciones/<slug:municipio>/<slug:localidad>/<slug:nivelacademico>/<areainteres>/<slug:dominio>/',views.updInst,name="filtrar_instituciones"),
    path('SigApp/updInformacion/<Ndirector>/<Ninstitucion>/',views.updInfo,name="modificar_datos"),
    path('SigApp/detalle/<idr>/<inst>',views.detalle, name='detalle'),
    path('SigApp/miInstitucion/<nombre>/',views.miInstitucion, name='miInstitucion'), 
    path('SigApp/updInfoEstadistica/<año>/<clave_ins>/',views.updInfoEstadistica, name='updInfoEstadistica'), 
    #path('SigApp/accounts/', include('accounts.urls')),
    path('SigApp/perfilAdmin',views.perfilAdmin, name='perfilAdmin'),
    path('SigApp/modificacionesAdmin',views.modificacionesAdmin, name='modificacionesAdmin'),
    path('SigApp/mostrarInstitucion/<nombre>/',views.mostrarInstitucion, name='mostrarInstitucion'),
    path('SigApp/mostrarRegistro/<nombre>/',views.mostrarRegistro, name='mostrarRegistro'),
    path('SigApp/modificaciones',views.modificacionesAdmin, name='modificaciones'),
    path('SigApp/SigMovil/<id>/<clave>',views.APIapp,name="SigMovil"),
    path('SigApp/registrosAdmin',views.registrosAdmin, name='registrosAdmin'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)



