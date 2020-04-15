from django.urls import path
from . import views
#https://weasyprint.readthedocs.io/en/latest/install.html

urlpatterns = [
    path('', views.index_user, name='inicio'),
    path('solicitud/validacion', views.validacion, name='validacion'),
    path('solicitud/', views.solicitud, name='solicitud'),
    path('solicitud/crear/', views.solicitud_insert, name='solicitud_insert'),
    #Subida de archivos
    path('solicitud/institucional', views.SInstitucional, name='institucionalSup'),
    path('solicitud/curricular', views.SCurricular, name='curricularSup'),
    path('solicitud/academica', views.SAcademica, name='academicaSup'),
    path('solicitud/media_superior', views.SMedSuperior, name='medSuperior'),
    path('solicitud/enviada', views.finSolicitud, name='finSolicitud'),
    path('acuerdos', views.acuerdos, name='acuerdos'),

    path('estadoSolicitud/<usuario>/<solicitud>', views.estatus, name='estado'),
    path('estadoSolicitud/<usuario>/H/<solicitud>/', views.historial, name='historial'),
    path('estadoSolicitud/<usuario>/H/<solicitud>/archivos', views.verArchivos,name='verArchivos'),
    path('estadoSolicitud/<usuario>/H/<solicitud>/subirArchivos/', views.subirArchivos, name='subirArchivos'),
    path('estadoSolicitud/<usuario>/H/<solicitud>/subirArchivos/terminar/',
         views.terminarSubArchivos, name='terminarSubArchivos'),

    path('notificaciones/', views.notificacionUsuario, name='notificacionUsuario'),
    path('hitorialNotificaciones/', views.historialNotificacionesUsuario, name='hitorialNotificacionUsuario'),
    # Rutas de usuario personal del departamento
    path('admin/', views.administrador, name='admin'),
    path('admin/historialNotificaciones/',views.historialNotificacionesAdmin, name='hitorialNotificacionAdmin'),
    path('admin/<solicitud>', views.administradorSolicitud, name='adminSolicitud'),
    path('admin/notificaciones/G', views.notificacionAdministrador, name='notificacionAdmin'),
    path('admin/archivos/<solicitud>', views.revision, name='solicitudArchivos'),
    path('admin/archivos/<solicitud>/institucional/', views.revisionCInstitucional, name='revInstitucional'),
    path('admin/archivos/<solicitud>/curricular/', views.revisionCCurricular, name='revCurricular'),
    path('admin/archivos/<solicitud>/academica/', views.revisionCAcademica, name='revAcademica'),
    path('admin/archivos/<solicitud>/medSuperior/', views.revisionCMedSuperior, name='revMedSuperior'),
    path('admin/archivos/<solicitud>/comentarios/mostrar/<carpeta>', views.comentariosMostrar, name='comentariosSolicitudMostrar'),
    path('admin/archivos/<solicitud>/comentarios/eliminar/<idArchivo>/<carpeta>', views.comentariosEliminar, name='comentariosSolicitudEliminar'),
    path('admin/archivos/<solicitud>/comentarios/<idArchivo>/<carpeta>', views.comentariosSolicitud, name='comentariosSolicitud'),
    path('admin/archivos/<solicitud>/terminado', views.comentariosTerminado, name='comentariosSolicitudTerminado'),
    path('admin/archivos/<solicitud>/entregoDocumentos', views.entregoDocumentosFisicos, name='entregoDocumentos'),
    path('admin/historialActividades/', views.historialActividades, name='historialActivi'),
    path('admin/finProceso/<solicitud>/', views.finProceso, name='finProceso'),
    #path('admin/verpdf/', views.verpdf, name='verpdf'),
    path('generate/pdf/<id>', views.Pdf.as_view(), name='generate_pdf'),
]
