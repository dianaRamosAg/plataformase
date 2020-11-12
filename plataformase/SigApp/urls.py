from django.urls import path, include
from .import views
from django.conf import settings
from django.conf.urls.static import static



app_name ='SigApp'
#SigMovilFiltros/MEDIA-SUPERIOR/empty/PRIVADA/empty/
urlpatterns = [

    path('',views.index, name='index'),
    path('index',views.index, name='index'),

    path('nuevaBase', views.nuevaBase, name='nuevaBase'),
    
    path('inicio', views.inicio, name='inicio'),
    path('actas_departamento', views.actas_departamento, name='actas_departamento'),
    path('bandeja_quejas', views.bandeja_quejas, name='bandeja_quejas'),
    path('historial_institucion', views.historial_institucion, name='historial_institucion'),
    path('programar_superv', views.programar_superv, name='programar_superv'),

    path('infosistemas',views.infosistemas,name='infosistemas'),
    path('perfilinstitucion/<id>/<claveescuela>/',views.perfilinstitucion,name='perfilinstitucion'),
    path('actasdesupervision',views.actasdesupervision,name='actasdesupervision'),


    path('instituciones/<id>/<slug:clave>',views.instituciones, name='instituciones'),  
    path('institucionesUbicacion/<id>/<slug:clave>',views.institucionesUbicacion, name='institucionesUbicacion'),  
    

    path('localizador',views.localizador, name='localizador'), 
    path('localizarInst/<clave>',views.localizarInst, name='localizarInst'),

    path('SigMovilFiltros/<slug:mediasuperior>/<slug:superior>/<slug:privada>/<slug:publica>/',views.APIappFiltros,name="filtros"),
    path('updl/<int:mun>',views.selecccion_municipio, name='selectMun'),
    path('updInstituciones/<slug:municipio>/<slug:localidad>/<slug:nivelacademico>/<areainteres>/<slug:dominio>/',views.updInst,name="filtrar_instituciones"),
    path('updInformacion/<Ndirector>/<Ninstitucion>/',views.updInfo,name="modificar_datos"),
    path('detalle/<idr>/<inst>',views.detalle, name='detalle'),
    
    path('miInstitucion/<id>/<id_dep>/',views.miInstitucion, name='miInstitucion'), 
    path('selectInstitucion2/<id>/',views.selectInstitucion, name='selectInstitucion'), 
    
    path('updInfoEstadistica/<año>/<clave_ins>/',views.updInfoEstadistica, name='updInfoEstadistica'), 

    path('modEstadistica/<clave>/<id_dep>/',views.modEstadistica, name='modEstadistica'), 
    path('estadistica/<clave>/<claveE>/<id_dep>/',views.solicitaModEstadistica, name='solicitaModEstadistica'), 

    #path('SigApp/accounts/', include('accounts.urls')),
    path('perfilAdmin',views.perfilAdmin, name='perfilAdmin'),

    path('modificacionesAdmin/<id>/',views.modificacionesAdmin, name='modificacionesAdmin'),
    path('mostrarInstitucion/<nombre>/',views.mostrarInstitucion, name='mostrarInstitucion'),
    path('mostrarInstitucionEst/<claveC>/<claveE>/',views.mostrarInstitucionEst, name='mostrarInstitucionEst'),

    path('listado_historial/',views.listarHistorial, name='listarHistorial'),
    path('mostrar_historial/<id>/',views.mostrarHistorial, name='mostrarHistorial'),

    path('listado_historialEst/',views.listarHistorialEst, name='listarHistorialEst'),
    path('mostrar_historialEst/<id>/',views.mostrarHistorialEst, name='mostrarHistorialEst'),

    path('mostrarRegistro/<nombre>/',views.mostrarRegistro, name='mostrarRegistro'),
    
    path('SigMovil/<id>/<clave>',views.APIapp,name="SigMovil"),
    path('registrosAdmin',views.registrosAdmin, name='registrosAdmin'),
]
