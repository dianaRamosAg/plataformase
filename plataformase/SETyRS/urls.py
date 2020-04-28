from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    #urls del administrador
    path('admin/',login_required(views.index_admin), name='SETyRS_admin_index'), #INDEX

    #urls de la institucion SINODALES
    path('institucion/', login_required(views.index_institucion), name='SETyRS_institucion_index'), #INDEX
    path('institucion/nueva_solicitud_sinodal/', login_required(views.nueva_solicitud_sinodal), name='SETyRS_nueva_solicitud_sinodal'), #Vista para crear una nueva solicitud de sinodal
    path('institucion/nueva_solicitud_sinodal/crear', login_required(views.crear_solicitud_sinodal), name='SETyRS_crear_solicitud_sinodal'), #Metodo de creacion de una nueva solicitud de sinodal en la bd
    path('institucion/solicitud/sinodal/<int:id>/', login_required(views.detalle_solicitud_sinodal), name='SETyRS_detalle_solicitud_sinodal'), #Vista de detalle solicitud que redirige a una pagina deacuerdo al estado o fase de la solicitud
    path('institucion/solicitud/sinodal/<int:id>/agregar_sinodal/', login_required(views.agregar_sinodal), name='SETyRS_agregar_sinodal'), #Metodo para agregar un sinodal a la solicitud
    path('institucion/solicitud/sinodal/eliminar_sinodal/', login_required(views.eliminar_sinodal), name='SETyRS_eliminar_sinodal'), #Metodo para eliminar un sinodal de la solicitud
    path('institucion/solicitud/sinodal/editar_sinodal/', login_required(views.editar_sinodal), name='SETyRS_editar_sinodal'), #Metodo para editar un sinodal de la solicitud
    path('institucion/solicitud/sinodal/<int:id>/documentos', login_required(views.agregar_documentos_sinodales), name='SETyRS_agregar_documentos_sinodal'), #Metodo para avanzar a la fase de agregar documentos a los sinodales registrados
    path('institucion/solicitud/sinodal/<int:id>/agregar_documentos/', login_required(views.subir_documentos_sinodal), name='SETyRS_subir_documentos_sinodal'), #Metodo para subir los documentos de un sinodal
    path('institucion/solicitud/sinodal/<int:id>/editar_documentos/', login_required(views.editar_documentos_sinodal), name='SETyRS_editar_documentos_sinodal'), #Metodo para editar los documentos de un sinodal
    path('institucion/solicitud/sinodal/<int:id>/enviar_solicitud', login_required(views.finalizar_solicitud_sinodal), name='SETyRS_finalizar_solicitud_sinodal'), #Metodo para finalizar la solicitud y "enviarla" al departamento correspondiente

    path('institucion/solicitudes/sinodales', login_required(views.lista_solicitudes_sinodales), name='SETyRS_solicitudes_sinodales'), #Vista de solicitudes de sinodales realizadas

    #urls de notificaciones de institucion
    path('institucion/notificacion/<int:id>', login_required(views.leer_notificacion), name='leerNotificacion'), #Metodo para marcar como leida la notificacion

]