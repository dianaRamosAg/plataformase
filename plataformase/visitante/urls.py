from django.urls import path
from . import views
from . import views

#app_name="visitante"

urlpatterns = [
    path('', views.index, name='index'),
    path('notificacionsc/validar/signuprv/', views.regUser, name='signuprv'),
    path('menuinstitucion/', views.menuinstitucion, name='menuinstitucion'),
    path('menuadmin/', views.menuadmin, name='menuadmin'),
    path('menudepartamento/', views.menudepartamento, name='menudepartamento'),
    path('control/', views.control, name='control'),
    path('menuvisitante/', views.menuvisitante, name='menuvisitante'),
     path('cuentavisitante/', views.cuentavisitante, name='cuentavisitante'),
     path('perfiluser/', views.perfiluser, name='perfiluser'),
     path('actualizarperfilusr/', views.actualizarperfilusr, name='actualizarperfilusr'),
     path('notificacion/', views.notificacion, name='notificacion'),
     path('notificaciones/', views.notificacionadmon, name='notificacionadmon'),
     path('solicitudcuenta/', views.regVisit, name='solicitudcuenta'),
     path('solicitudenviada/', views.modal, name='solicitudenviada'),
     path('notificacionsc/', views.notificacionsc, name='notificacionsc'),
     path('notificacionsc/validar/<email>/',views.validar, name='validar'),
     path('notificacionsc/validar/<email2>/cancelarsolicitud/<email>',views.cancelarsolicitud, name='cancelarsolicitud'),
    #  path('signuprv/',views.regUser, name='signuprv'),
        
]