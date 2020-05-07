from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name ='SigApp'
#SigMovilFiltros/MEDIA-SUPERIOR/empty/PRIVADA/empty/
urlpatterns = [
    path('',views.index, name='index'),
    #path('instituciones',views.instituciones, name='instituciones'), 
    path('instituciones/<id>/<slug:clave>',views.instituciones, name='instituciones'),   
    path('localizador',views.localizador, name='localizador'), 
    path('SigMovilFiltros/<slug:mediasuperior>/<slug:superior>/<slug:privada>/<slug:publica>/',views.APIappFiltros,name="filtros"),
    path('updl/<int:mun>',views.selecccion_municipio, name='selectMun'),
    path('updInstituciones/<slug:municipio>/<slug:localidad>/<slug:nivelacademico>/<areainteres>/<slug:dominio>/',views.updInst,name="filtrar_instituciones"),
    path('updInformacion/<Ndirector>/<Ninstitucion>/',views.updInfo,name="modificar_datos"),
    path('detalle/<idr>/<inst>',views.detalle, name='detalle'),
    path('miInstitucion/<nombre>/',views.miInstitucion, name='miInstitucion'), 
    path('updInfoEstadistica/<año>/<clave_ins>/',views.updInfoEstadistica, name='updInfoEstadistica'), 
    #path('SigApp/accounts/', include('accounts.urls')),
    path('perfilAdmin',views.perfilAdmin, name='perfilAdmin'),
    path('modificacionesAdmin',views.modificacionesAdmin, name='modificacionesAdmin'),
    path('mostrarInstitucion/<nombre>/',views.mostrarInstitucion, name='mostrarInstitucion'),
    path('mostrarRegistro/<nombre>/',views.mostrarRegistro, name='mostrarRegistro'),
    path('modificaciones',views.modificacionesAdmin, name='modificaciones'),
    path('SigMovil/<id>/<clave>',views.APIapp,name="SigMovil"),
    path('registrosAdmin',views.registrosAdmin, name='registrosAdmin'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)



