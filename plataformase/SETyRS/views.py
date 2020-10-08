from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.utils import timezone
from datetime import date
from django.contrib import messages
from django.http import JsonResponse
from .models import *
from login.models import CustomUser
from .forms import *
from django.conf import settings
from RVOES.models import Departamento
from login.models import UsuarioInstitucion
from .render import Render
from django.core.mail import send_mail, EmailMessage
from django.core.files.storage import FileSystemStorage
from django.core import serializers
# VISTAS DEL ADMINISTRADOR SINODALES-----------------------------------------------------------------------------
#.
# el departamento de dirección es el unico que puede ver e interactuar con las solicitudes de ambos niveles educativos (superior y media superior)
#dirección: 2
#superior: 3
#media superior: 4

# funcion que retorna el index del administrador con el contexto de acuerdo al departamento del usuario
def index_admin(request):
    #si el usuario no pertenece a cualquiera de estos 3 departamentos, se mostrará el error 404
    if request.user.departamento_id==2 or request.user.departamento_id==3 or request.user.departamento_id==4 or request.user.departamento_id==1:
        dep = get_object_or_404(Departamento, pk=request.user.departamento_id)
        num_notifi = contarNotificacionesadmin(request.user.departamento_id) # cuenta las notificaciones que no han sido leidas y retorna el total
        if request.user.departamento_id == 2: #si el usuario pertenece al departamento DIRECCION
            notificacion = NotificacionAdmin.objects.filter().order_by('-fecha') #Recupera las notificaciones del administrador

        elif request.user.departamento_id == 3: #si el usuario pertenece al departamento SUPERIOR
            notificacion = NotificacionAdmin.objects.filter(nivel_educativo=2).order_by('-fecha') #Recupera las notificaciones del administrador

        elif request.user.departamento_id == 4: #si el usuario pertenece al departamento MEDIA SUPERIOR
            notificacion = NotificacionAdmin.objects.filter(nivel_educativo=1).order_by('-fecha') #Recupera las notificaciones del administrador

        elif request.user.departamento_id == 1: #si el usuario pertenece al departamento CONTROL ESCOLAR
            notificacion = NotificacionAdmin.objects.filter(tipo_solicitud=1).order_by('-fecha') #Recupera las notificaciones del administrador
        
        context = {'departamento':dep,'notificacion':notificacion,'notificaciones':num_notifi}
        return render(request,'admins/index_admin.html', context)
    else:
        raise Http404("El usuario no tiene permiso de ver esta página")

#funcion que retorna la plantilla de revisión de solicitud de sinodal
def revisar_solicitud_sinodal(request, id):
    if request.user.departamento_id==2 or request.user.departamento_id==3 or request.user.departamento_id==4:
        solicitud = get_object_or_404(SolicitudSinodal, pk=id)
        if solicitud.fase == 3: #si la solicitud no está en fase 3 quiere decir que aún no a sido terminada por la institución, por ende no debe visualizarse
            dep = get_object_or_404(Departamento, pk=request.user.departamento_id)
            sinodales = ArchivosSinodales.objects.select_related('sinodal').filter(sinodal__id_solicitud_id=id).order_by('sinodal__nombre_sinodal')
            for s in sinodales:
                if s.sinodal.estatus == 3:
                    s.sinodal.estatus = 'Rechazado'
                elif s.sinodal.estatus == 1:
                    s.sinodal.estatus = 'Pendiente'
                elif s.sinodal.estatus == 2:
                    s.sinodal.estatus = 'Aceptado'
            num_notifi = contarNotificacionesadmin(request.user.departamento_id)
            context = {'departamento':dep,'lista_sinodales': sinodales,'solicitud':solicitud,'notificaciones':num_notifi}
            if request.user.departamento_id == 2:
                notificacion = NotificacionAdmin.objects.filter().order_by('-fecha')
                context.update({'notificacion':notificacion})
                return render(request, 'admins/sinodales/revisar_solicitud_sinodal.html', context)

            elif request.user.departamento_id == 3 and solicitud.nivel_educativo == 2: #nivel educativo: 2 es superior y 1 es media superior
                notificacion = NotificacionAdmin.objects.filter(nivel_educativo=2).order_by('-fecha')
                context.update({'notificacion':notificacion})
                return render(request, 'admins/sinodales/revisar_solicitud_sinodal.html', context)

            elif request.user.departamento_id == 4 and solicitud.nivel_educativo == 1:
                notificacion = NotificacionAdmin.objects.filter(nivel_educativo=1).order_by('-fecha')
                context.update({'notificacion':notificacion})
                return render(request, 'admins/sinodales/revisar_solicitud_sinodal.html', context)
            else:
                raise Http404("El usuario no tiene permiso de ver esta página")
        else:
            raise Http404("La solicitud no es valida o no existe")
    else:
        raise Http404("El usuario no tiene permiso de ver esta página")

# Metodo que retorna la plantilla del listado de solicitudes de sinodales con su respectivo departamento
def lista_solicitudes_sinodales_admin(request):
    if request.user.departamento_id==2 or request.user.departamento_id==3 or request.user.departamento_id==4:
        dep = get_object_or_404(Departamento, pk=request.user.departamento_id)
        num_notifi = contarNotificacionesadmin(request.user.departamento_id)
        if request.user.departamento_id == 2:
            notificacion = NotificacionAdmin.objects.filter().order_by('-fecha')
            solicitudes = SolicitudSinodal.objects.filter(fase=3).order_by('-id')
        elif request.user.departamento_id == 3:
            notificacion = NotificacionAdmin.objects.filter(nivel_educativo=2).order_by('-fecha')
            solicitudes = SolicitudSinodal.objects.filter(fase=3, nivel_educativo=2).order_by('-id')
        elif request.user.departamento_id == 4:
            notificacion = NotificacionAdmin.objects.filter(nivel_educativo=1).order_by('-fecha')
            solicitudes = SolicitudSinodal.objects.filter(fase=3, nivel_educativo=1).order_by('-id')
        for s in solicitudes:
            if s.estatus == 2:
                s.estatus = 'Pendiente'
            elif s.estatus == 3:
                s.estatus = 'Revisada'
        context = {'departamento':dep,'solicitudes': solicitudes,'notificacion':notificacion,'notificaciones':num_notifi}
        return render(request,'admins/sinodales/lista_solicitud_sinodales.html', context)
    else:
        raise Http404("El usuario no tiene permiso de ver esta página")

#Metodo que retorna la plantilla del listado de sinodales ya aceptados por el departamento
def lista_sinodales(request):
    if request.user.departamento_id==2 or request.user.departamento_id==3 or request.user.departamento_id==4:
        dep = get_object_or_404(Departamento, pk=request.user.departamento_id)
        num_notifi = contarNotificacionesadmin(request.user.departamento_id)
        if request.user.departamento_id == 2:
            sinodales = ArchivosSinodales.objects.select_related('sinodal').filter(sinodal__estatus=2).order_by('sinodal__rfc')
            notificacion = NotificacionAdmin.objects.filter().order_by('-fecha')
        elif request.user.departamento_id == 3:
            sinodales = ArchivosSinodales.objects.select_related('sinodal').filter(sinodal__estatus=2, sinodal__nivel_educativo=2).order_by('sinodal__rfc')
            notificacion = NotificacionAdmin.objects.filter(nivel_educativo=2).order_by('-fecha')
        elif request.user.departamento_id == 4:
            sinodales = ArchivosSinodales.objects.select_related('sinodal').filter(sinodal__estatus=2, sinodal__nivel_educativo=1).order_by('sinodal__rfc')
            notificacion = NotificacionAdmin.objects.filter(nivel_educativo=1).order_by('-fecha')
        context = {'departamento':dep,'sinodales':sinodales,'notificacion':notificacion,'notificaciones':num_notifi}
        return render(request,'admins/sinodales/lista_sinodales.html', context)
    else:
        raise Http404("El usuario no tiene permiso de ver esta página")

#Metodo que retorna la plantilla del historial de movimientos de sinodales en el departamento, saber quien y cuando fue aceptado o rechazado un sinodal
def historial_sinodales(request):
    if request.user.departamento_id==2 or request.user.departamento_id==3 or request.user.departamento_id==4:
        dep = get_object_or_404(Departamento, pk=request.user.departamento_id)
        num_notifi = contarNotificacionesadmin(request.user.departamento_id)
        if request.user.departamento_id == 2:
            notificacion = NotificacionAdmin.objects.filter().order_by('-fecha')
            historial = Historial_admins_sinodal.objects.select_related('user','sinodal').order_by('sinodal_id')
        elif request.user.departamento_id == 3:
            notificacion = NotificacionAdmin.objects.filter(nivel_educativo=2).order_by('-fecha')
            historial = Historial_admins_sinodal.objects.select_related('user','sinodal').filter(nivel_educativo=2).order_by('sinodal_id')
        elif request.user.departamento_id == 4:
            notificacion = NotificacionAdmin.objects.filter(nivel_educativo=1).order_by('-fecha')
            historial = Historial_admins_sinodal.objects.select_related('user','sinodal').filter(nivel_educativo=1).order_by('sinodal_id')
        for h in historial:
            if h.estatus:
                h.estatus = 'Aceptado'
            else:
                h.estatus = 'Rechazado'
            if h.user.departamento_id == 2:
                h.user.departamento_id = 'Dirección'
            elif h.user.departamento_id == 3:
                h.user.departamento_id = 'Superior'
            elif h.user.departamento_id == 4:
                h.user.departamento_id = 'Media Superior'
        context = {'departamento':dep,'notificacion':notificacion,'notificaciones':num_notifi,'historial':historial}
        return render(request,'admins/sinodales/historial_actividades.html', context)
    else:
        raise Http404("El usuario no tiene permiso de ver esta página")



# FUNCIONES DEL ADMINISTRADOR SINODALES--------------------------------------------------------------------------------------------



# Metodo que retorna el total de notificaciones que no han sido leidas dependiendo del departamento del usuario activo
def contarNotificacionesadmin(departamento):
    if departamento == 2:
        notificacion = NotificacionAdmin.objects.filter(visto=False).count()
        return notificacion
    elif departamento == 3:
        notificacion = NotificacionAdmin.objects.filter(visto=False, nivel_educativo=2).count()
        return notificacion
    elif departamento == 4:
        notificacion = NotificacionAdmin.objects.filter(visto=False, nivel_educativo=1).count()
        return notificacion

# Metodo que cambia el estado de la notificacion a leida y redirige a la vista de revision de solicitud, si el tipo de
# solicitud es 1 redirige a la pagina de revision de solicitudes de examen a titulo, si es 2 a la de sinodales
def leer_notificacion_admin(request, id):
    if request.user.departamento_id == 2 or request.user.departamento_id == 3 or request.user.departamento_id == 4:
        notificacion=get_object_or_404(NotificacionAdmin, pk=id)
        if notificacion.visto == False:
            notificacion.visto = True
            notificacion.save()
        if notificacion.tipo_solicitud == 1:
            return redirect('SETyRS_revisar_solicitud_examen', notificacion.solicitud_id)
        else:
            return redirect('SETyRS_revisar_solicitud_sinodal', notificacion.solicitud_id)
    else:
        raise Http404('El usuario no tiene permiso de ver esta página')

def aceptar_sinodal(request, id):
    if request.user.departamento_id == 2 or request.user.departamento_id == 3 or request.user.departamento_id == 4:
        if request.method == 'POST':
            id_sinodal = request.POST['id_sino']
            solicitud = get_object_or_404(SolicitudSinodal, pk=id)
            sinodal = get_object_or_404(Sinodales, pk=id_sinodal)
            sinodal.estatus = 2
            sinodal.save()
            if solicitud.estatus != 3:
                solicitud.estatus = 3
                solicitud.save()
                msg = 'Se ha revisado tu solicitud de sinodales. Folio: ' + str(id)
                notificacion = Notificaciones(descripcion=msg, fecha=timezone.now(), solicitud_id=id,tipo_solicitud=2,user_id=solicitud.user_id)
                notificacion.save()
            historial = Historial_admins_sinodal(user_id=request.user.id,sinodal_id=id_sinodal,fecha=timezone.now(),solicitud_id=id,
                                                    estatus=True,nivel_educativo=solicitud.nivel_educativo)
            historial.save()
            return redirect('SETyRS_revisar_solicitud_sinodal', id)
        else:
            raise Http404('Página no encontrada')
    else:
        raise Http404('El usuario no tiene permiso de ver esta página')

def rechazar_sinodal(request, id):
    if request.user.departamento_id == 2 or request.user.departamento_id == 3 or request.user.departamento_id == 4:
        if request.method == 'POST':
            id_sinodal = request.POST['id_sino']
            comentarios = request.POST['comentarios']
            solicitud = get_object_or_404(SolicitudSinodal, pk=id)
            sinodal = get_object_or_404(Sinodales, pk=id_sinodal)
            sinodal.estatus = 3
            sinodal.save()
            if solicitud.estatus != 3:
                solicitud.estatus = 3
                solicitud.save()
                msg = 'Se ha revisado tu solicitud de sinodales con folio: ' + str(id)
                notificacion = Notificaciones(descripcion=msg, fecha=timezone.now(), solicitud_id=id,tipo_solicitud=2,user_id=solicitud.user_id)
                notificacion.save()
            historial = Historial_admins_sinodal(user_id=request.user.id,sinodal_id=id_sinodal,solicitud_id=id,fecha=timezone.now(),
                                                    comentarios=comentarios,nivel_educativo=solicitud.nivel_educativo)
            historial.save()
            return redirect('SETyRS_revisar_solicitud_sinodal', id)
        else:
            raise Http404('Página no encontrada')
    else:
        raise Http404('El usuario no tiene permiso de ver esta página')


#VISTAS DEL ADMINISTRADOR EXAMENES A TITULO----------------------------------------------------------------------------------------


def lista_solicitudes_examenes_admin(request):
    if request.user.departamento_id==2 or request.user.departamento_id==3 or request.user.departamento_id==4 or request.user.departamento_id==1:
        dep = get_object_or_404(Departamento, pk=request.user.departamento_id)
        num_notifi = contarNotificaciones(request.user.departamento_id)
        if request.user.departamento_id==2:
            solicitudes = SolicitudExamen.objects.select_related('user').filter(fase=3).order_by('-id')
            notificacion = NotificacionAdmin.objects.filter().order_by('-fecha')
            
        elif request.user.departamento_id==3:
            solicitudes = SolicitudExamen.objects.filter(fase=3,nivel_educativo=2).order_by('-id')
            notificacion = NotificacionAdmin.objects.filter(nivel_educativo=2).order_by('-fecha')
            
        elif request.user.departamento_id==4:
            solicitudes = SolicitudExamen.objects.filter(fase=3,nivel_educativo=1).order_by('-id')
            notificacion = NotificacionAdmin.objects.filter(nivel_educativo=1).order_by('-fecha')

        elif request.user.departamento_id==1:
            solicitudes = SolicitudExamen.objects.filter(fase=3,estatus=3).order_by('-id')
            notificacion = None
        
        context = {'departamento':dep, 'solicitudes': solicitudes, 'notificacion':notificacion,'notificaciones':num_notifi}
        for s in solicitudes:
            if s.estatus == 2:
                s.estatus = 'Pendiente'
            elif s.estatus == 3:
                s.estatus = 'Aprobada'
            elif s.estatus == 4:
                s.estatus = 'Rechazada'
        return render(request,'admins/examenes/lista_solicitud_examenes.html', context)
    else:
        raise Http404("El usuario no tiene permiso de ver esta página")

def revisar_solicitud_examen(request, id):
    if request.user.departamento_id==2 or request.user.departamento_id==3 or request.user.departamento_id==4 or request.user.departamento_id==1:
        solicitud = get_object_or_404(SolicitudExamen, pk=id)
        if solicitud.fase == 3:
            dep = get_object_or_404(Departamento, pk=request.user.departamento_id)
            alumnos = ArchivosAlumnos.objects.select_related('alumno').filter(solicitud_id=id).order_by('alumno__nombre_alumno')
            if solicitud.estatus == 2:
                solicitud.estatus = 'Pendiente'
            elif solicitud.estatus == 3:
                solicitud.estatus = 'Aceptada'
            elif solicitud.estatus == 4:
                solicitud.estatus = 'Rechazada'
            num_notifi = contarNotificaciones(request.user.departamento_id)
            presidente = ArchivosSinodales.objects.select_related('sinodal').get(sinodal_id = solicitud.id_presidente)
            secretario = ArchivosSinodales.objects.select_related('sinodal').get(sinodal_id = solicitud.id_secretario)
            vocal =  ArchivosSinodales.objects.select_related('sinodal').get(sinodal_id = solicitud.id_vocal)
            user = request.user
            context = {'departamento':dep,'lista_alumnos': alumnos, 'solicitud':solicitud,'p':presidente,'s':secretario,'v':vocal,'notificaciones':num_notifi, 'usuario': user}

            if request.user.departamento_id == 2:
                notificacion = NotificacionAdmin.objects.filter().order_by('-fecha')
                context.update({'notificacion':notificacion})
                return render(request, 'admins/examenes/revisar_solicitud_examen.html', context)

            elif request.user.departamento_id == 3 and solicitud.nivel_educativo == 2: #nivel educativo: 2 es superior y 1 es media superior
                notificacion = NotificacionAdmin.objects.filter(nivel_educativo=2).order_by('-fecha')
                context.update({'notificacion':notificacion})
                return render(request, 'admins/examenes/revisar_solicitud_examen.html', context)
            
            elif request.user.departamento_id == 4 and solicitud.nivel_educativo == 1:
                notificacion = NotificacionAdmin.objects.filter(nivel_educativo=1).order_by('-fecha')
                context.update({'notificacion':notificacion})
                return render(request, 'admins/examenes/revisar_solicitud_examen.html', context)
            elif request.user.departamento_id == 1:
                notificacion = None
                context.update({'notificacion':notificacion})
                return render(request, 'admins/examenes/revisar_solicitud_examen.html', context)
        else:
            raise Http404("El usuario no tiene permiso de ver esta página")        
    else:
        raise Http404("El usuario no tiene permiso de ver esta página")

def historial_examenes(request):
    if request.user.departamento_id==2 or request.user.departamento_id==3 or request.user.departamento_id==4:
        dep = get_object_or_404(Departamento, pk=request.user.departamento_id)
        num_notifi = contarNotificacionesadmin(request.user.departamento_id)
        if request.user.departamento_id == 2:
            notificacion = NotificacionAdmin.objects.filter().order_by('-fecha')
            historial = Historial_admins_examen.objects.select_related('user','solicitud__user').order_by('fecha')
        elif request.user.departamento_id == 3:
            notificacion = NotificacionAdmin.objects.filter(nivel_educativo=2).order_by('-fecha')
            historial = Historial_admins_examen.objects.select_related('user').filter(nivel_educativo=2).order_by('fecha')
        elif request.user.departamento_id == 4:
            notificacion = NotificacionAdmin.objects.filter(nivel_educativo=1).order_by('-fecha')
            historial = Historial_admins_examen.objects.select_related('user').filter(nivel_educativo=1).order_by('fecha')
        for h in historial:
            if h.estatus:
                h.estatus = 'Aprobada'
            else:
                h.estatus = 'Rechazada'
            if h.user.departamento_id == 2:
                h.user.departamento_id = 'Dirección'
            elif h.user.departamento_id == 3:
                h.user.departamento_id = 'Superior'
            elif h.user.departamento_id == 4:
                h.user.departamento_id = 'Media Superior'
        context = {'departamento':dep,'notificacion':notificacion,'notificaciones':num_notifi,'historial':historial}
        return render(request,'admins/examenes/historial_actividades.html', context)
    else:
        raise Http404("El usuario no tiene permiso de ver esta página")


#FUNCINES DEL ADMINISTRADOR EXAMENES A TITULO----------------------------------------------------------------------------------------


def aceptar_solicitud(request, id):
    if request.user.departamento_id == 2 or request.user.departamento_id == 3 or request.user.departamento_id == 4:
        if request.method == 'POST':
            solicitud = get_object_or_404(SolicitudExamen, pk=id)
            solicitud.estatus = 3
            solicitud.save()
            h_solicitud = Historial_admins_examen(user_id = request.user.id, solicitud_id = id,fecha=timezone.now(), estatus=True, nivel_educativo=solicitud.nivel_educativo)
            h_solicitud.save()
            
            #Aqui poner el codigo para enviar el correo de aceptación a control escolar,dirección y al departamento correspondiente
            if solicitud.nivel_educativo == 1:
                email = EmailMessage('Una nueva solicitud de examen ha sido aceptada en la plataforma','Una nueva solicitud de examen a titulo fue aceptada en la plataforma. Puede revisarla en el siguiente enlace:\n '+'https://ssemssicyt.nayarit.gob.mx/SETyRS/admin/solicitud/examen_a_titulo/'+str(solicitud.id)+'/',
                             to=['control.escolar@educacion.nayarit.gob.mx','direccionmediaysuperior@educacion.nayarit.gob.mx','superior@educacion.nayarit.gob.mx'])
                email.send()
            elif solicitud.nivel_educativo == 2:
                email = EmailMessage('Una nueva solicitud de examen ha sido aceptada en la plataforma','Una nueva solicitud de examen a titulo fue aceptada en la plataforma. Puede revisarla en el siguiente enlace:\n '+'https://ssemssicyt.nayarit.gob.mx/SETyRS/admin/solicitud/examen_a_titulo/'+str(solicitud.id)+'/',
                             to=['control.escolar@educacion.nayarit.gob.mx','direccionmediaysuperior@educacion.nayarit.gob.mx','media.superior@educacion.nayarit.gob.mx'])
                email.send()
            msg = 'Solicitud de examenes a titulo ¡APROBADA!. Folio: ' + str(id)
            notificacion = Notificaciones(descripcion=msg, fecha=timezone.now(), solicitud_id=id,tipo_solicitud=1,user_id=solicitud.user_id)
            notificacion.save()
            return redirect('SETyRS_revisar_solicitud_examen', id)
        else:
            raise Http404('Página no encontrada')
    else:
        raise Http404('El usuario no tiene permiso de ver esta página')

def rechazar_solicitud(request, id):
    if request.user.departamento_id == 2 or request.user.departamento_id == 3 or request.user.departamento_id == 4:
        if request.method == 'POST':
            solicitud = get_object_or_404(SolicitudExamen, pk=id)
            solicitud.estatus = 4
            solicitud.save()
            comentarios = request.POST['comentarios']
            h_solicitud = Historial_admins_examen(user_id = request.user.id,solicitud_id = id,fecha=timezone.now(),comentarios=comentarios,nivel_educativo=solicitud.nivel_educativo)
            msg = 'Solicitud de examenes a titulo RECHAZADA. Folio: ' + str(id)
            notificacion = Notificaciones(descripcion=msg, fecha=timezone.now(), solicitud_id=id,tipo_solicitud=1,user_id=solicitud.user_id)
            notificacion.save()
            h_solicitud.save()
            return redirect('SETyRS_revisar_solicitud_examen', id)
        else:
            raise Http404('Página no encontrada')
    else:
        raise Http404('El usuario no tiene permiso de ver esta página')


# VISTAS DE LA INSTITUCION SINODALES-----------------------------------------------------------------------------


#funcion que retorna el index del usuario institucion
def index_institucion(request):
    if request.user.tipo_usuario=='1' and request.user.tipo_persona=='2':
        notificacion = Notificaciones.objects.filter(user_id=request.user.id).order_by('-fecha')
        num_notifi = contarNotificaciones(request.user.id)
        context = {'notificacion':notificacion,'notificaciones':num_notifi}
        return render(request, 'institucion/index_institucion.html', context)
    else: 
        raise Http404("El usuario no tiene permiso de ver esta página")

# funcion que retorna la plantilla de nueva solicitud de sinodal
def nueva_solicitud_sinodal(request):
    if request.user.tipo_usuario=='1' and request.user.tipo_persona=='2':
        centrosRegistrados = UsuarioInstitucion.objects.filter(id_usuariobase_id=request.user.id)
        notificacion = Notificaciones.objects.filter(user_id=request.user.id).order_by('-fecha')
        num_notifi = contarNotificaciones(request.user.id)
        context = {'notificacion':notificacion,'notificaciones':num_notifi,'centrosRegistrados':centrosRegistrados}
        return render(request, 'institucion/sinodales/nueva_solicitud.html', context)
    else:
        raise Http404("El usuario no tiene permiso de ver esta página")

# funcion que retorna 3 plantillas diferentes de acuerdo a la fase o estatus en la que se encuentra la solicitud de sinodales
#Recibe el id de la solicitud
def detalle_solicitud_sinodal(request, id):
    if request.user.tipo_usuario=='1' and request.user.tipo_persona=='2':
        solicitud = get_object_or_404(SolicitudSinodal, pk=id)
        datos_escuela = UsuarioInstitucion.objects.get(cct=solicitud.CCT)
        print(datos_escuela)
        nivel = datos_escuela.nivel_educativo
        if solicitud.user_id == request.user.id:
            notificacion = Notificaciones.objects.filter(user_id=request.user.id).order_by('-fecha')
            num_notifi = contarNotificaciones(request.user.id)
            lista_sinodales = Sinodales.objects.filter(id_solicitud_id=id).order_by('nombre_sinodal')
            archivos = ArchivosSinodales.objects.filter(solicitud_id=id).order_by('id')
            context = {'nivel':nivel,'lista_sinodales': lista_sinodales, 'solicitud':solicitud, 'archivos':archivos, 'notificacion':notificacion,'notificaciones':num_notifi}
            if solicitud.fase == 1:
                return render(request, 'institucion/sinodales/agregar_sinodales.html', context)
            elif solicitud.fase == 2:
                return render(request, 'institucion/sinodales/agregar_documentos_sinodales.html', context)
            else:
                if solicitud.estatus == 2:
                    solicitud.estatus = 'Pendiente'
                if solicitud.estatus == 3:
                    solicitud.estatus = 'Revisada'
                for s in lista_sinodales:
                    if s.estatus == 1:
                        s.estatus = 'Pendiente'
                    elif s.estatus == 2:
                        s.estatus = 'Aceptado'
                    else:
                        s.estatus = 'Rechazado'
                historial_rechazo = Historial_admins_sinodal.objects.select_related('sinodal').filter(solicitud_id=id, estatus=False).order_by('sinodal')
                context.update({'rechazados':historial_rechazo})
                return render(request, 'institucion/sinodales/informacion_solicitud_sinodal.html', context)
    else:
        raise Http404('El usuario no tiene permiso de ver esta pagina')

def upd_solicitud_sinodal(request):
    if request.method == 'POST':
        SolicitudSinodal.objects.filter(id=request.POST.get('idSoliSinod')).update(nivel_educativo=request.POST.get("nuevoNivel"))
        return JsonResponse("Updated",safe=False)

# funcion que retorna la plantilla donde se muestran todas las solicitudes de sinodales que han sido iniciadas o finalizadas
def lista_solicitudes_sinodales(request):
    if request.user.tipo_usuario=='1' and request.user.tipo_persona=='2':
        notificacion = Notificaciones.objects.filter(user_id=request.user.id).order_by('-fecha')
        num_notifi = contarNotificaciones(request.user.id)
        data=SolicitudSinodal.objects.filter(user_id=request.user.id).order_by('-id')
        context = {"data":data, 'notificacion':notificacion,'notificaciones':num_notifi}
        for s in data:
            e = s.estatus
            if e==1:
                s.estatus = 'Incompleta'
            elif e==2:
                s.estatus = 'Pendiente'
            elif e==3:
                s.estatus = 'Revisada'
                
        return render(request, 'institucion/sinodales/lista_solicitudes_sinodales.html', context)
    
    else:
        raise Http404('El usuario no tiene permiso de ver esta pagina')


# FUNCIONES DE LA INSTITUCION SINODALES--------------------------------------------------------------------------


# Metodo que retorna el total de notificaciones no leidas por el usuario. Recibe el id del usuario logueado
def contarNotificaciones(id):
    notificacion = Notificaciones.objects.filter(user_id=id, visto=False).count()
    return notificacion

# Metodo guarda una solcitud de sinodales en la BD
def crear_solicitud_sinodal(request):
    if request.user.tipo_usuario=='1' and request.user.tipo_persona=='2':
        if request.method == 'POST':
            user_id = request.user.id
            centroTrabajo = request.POST["cct"]
            datos_escuela = UsuarioInstitucion.objects.get(cct=centroTrabajo)
            nivel = datos_escuela.nivel_educativo 
            if nivel == 3:
                solicitud = SolicitudSinodal(user_id=user_id, fecha=timezone.now(), institucion=request.user.first_name,nivel_educativo=nivel,CCT=centroTrabajo)
                solicitud.save()
            else:
                solicitud = SolicitudSinodal(user_id=user_id, fecha=timezone.now(), institucion=request.user.first_name,nivel_educativo=nivel,CCT=centroTrabajo)
                solicitud.save()
            msg = 'Nueva solicitud de sinodales. Folio: ' + str(solicitud.id) + '. Estatus: Incompleta'
            notificacion = Notificaciones(descripcion=msg, fecha=timezone.now(), solicitud_id=solicitud.id, tipo_solicitud=2, user_id=user_id)
            notificacion.save()
            return redirect('SETyRS_detalle_solicitud_sinodal', solicitud.id)
        else:
            return redirect('SETyRS_nueva_solicitud_sinodal')
    else:
        raise Http404('El usuario no tiene permiso de ver esta pagina')

# Metodo que agrega en la BD sinodales para la solicitud. Recibe el id de la solicitud 
def agregar_sinodal(request, id):
    if request.user.tipo_usuario=='1' and request.user.tipo_persona=='2':
        if request.method == 'POST':
            nombre=request.POST["nombre_sinodal"]
            curp=request.POST["curp"]
            rfc=request.POST["rfc"]
            grado=request.POST["grado_academico"]
            sino_count = Sinodales.objects.filter(curp=curp, institucion=request.user.first_name,estatus=2).count()
            comprobar_duplicidad = Sinodales.objects.filter(curp=curp, institucion=request.user.first_name)
            solicitud = SolicitudSinodal.objects.get(id=id)
            nivel_sinodales = solicitud.nivel_educativo
            if comprobar_duplicidad and sino_count>=1:
            
                error = 'Este sinodal ya existe en su registro'
                messages.error(request, error)
                return redirect('SETyRS_detalle_solicitud_sinodal',id)
            else:
                sinodal = Sinodales(nombre_sinodal=nombre, curp=curp, rfc=rfc,grado_academico=grado, id_solicitud_id=id, user_id=request.user.id, institucion=request.user.first_name,nivel_educativo=nivel_sinodales)
                sinodal.save()
                return redirect('SETyRS_detalle_solicitud_sinodal',id)
    else:
        raise Http404('El usuario no tiene permiso de ver esta pagina')

# Metodo que elimina un sinodal de la BD
def eliminar_sinodal(request):
    if request.user.tipo_usuario=='1' and request.user.tipo_persona=='2':
        if request.method == 'POST':
            idSinodal = request.POST["idSin"]
            sinodal = Sinodales.objects.get(pk=idSinodal)
            solicitud = sinodal.id_solicitud_id
            sinodal.delete()
            return redirect('SETyRS_detalle_solicitud_sinodal', solicitud)
    else:
        raise Http404('El usuario no tiene permiso de ver esta pagina')

# Metodo para editar la informacion de la BD de un sinodal
def editar_sinodal(request):
    if request.user.tipo_usuario=='1' and request.user.tipo_persona=='2':
        if request.method == 'POST':
            idSinodal = request.POST["idSino"]
            sinodal = Sinodales.objects.get(pk=idSinodal)
            sinodal.nombre_sinodal = request.POST["nombre_sinodal"]
            sinodal.curp = request.POST["curp"]
            sinodal.rfc = request.POST["rfc"]
            sinodal.grado_academico = request.POST["grado_academico"]
            sinodal.save()
            solicitud = sinodal.id_solicitud_id
            return redirect('SETyRS_detalle_solicitud_sinodal', solicitud)
    else:
        raise Http404('El usuario no tiene permiso de ver esta pagina')

#Metodo para cambiar de fase la solicitud. al hacerlo, redirige a detalle solicitud que muestra la siguiente pantalla
def agregar_documentos_sinodales(request, id):
    if request.user.tipo_usuario=='1' and request.user.tipo_persona=='2':
        if request.method == 'POST':
            solicitud = get_object_or_404(SolicitudSinodal, pk=id)
            solicitud.fase = 2
            solicitud.save()
            return redirect('SETyRS_detalle_solicitud_sinodal', id)
    else:
        raise Http404("El usuario no tiene permiso de ver esta página")

#Metodo para subir los documentos de los sinodales a la plataforma. la BD guarda la URL del archivo
def subir_documentos_sinodal(request, id):
    if request.user.tipo_usuario=='1' and request.user.tipo_persona=='2':
        if request.method == 'POST':
            form = ArchivosSinodalesForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
            else:
                error = 'Solo son validos los archivos PDF'
                messages.error(request, error)
            return redirect('SETyRS_detalle_solicitud_sinodal',id)
    else:
        raise Http404("El usuario no tiene permiso de ver esta página")

#Metodo para editar los documentos de los sinodales una vez que ya hayan sido subidos
def editar_documentos_sinodal(request, id):
    if request.user.tipo_usuario=='1' and request.user.tipo_persona=='2':
        if request.method == 'POST':
            docs = ArchivosSinodales.objects.get(sinodal_id = request.POST['sinodal'])
            if request.FILES:
                if 'curriculum' in request.FILES:
                    docs.curriculum.delete()
                    docs.curriculum = request.FILES['curriculum']
                if 'cedula' in request.FILES:
                    docs.cedula.delete()
                    docs.cedula = request.FILES['cedula']
                docs.save()
            return redirect('SETyRS_detalle_solicitud_sinodal', id)
    else:
        raise Http404("El usuario no tiene permiso de ver esta página")

#Metodo para cambiar la fase y el estatus de la solicitud, redirige a detalle solicitud para que se mestre la siguiente pagina
# tambien actualiza las notificaciones del usuario y del administrador
def finalizar_solicitud_sinodal(request, id):
    if request.user.tipo_usuario=='1' and request.user.tipo_persona=='2':
        if request.method == 'POST':
            solicitud = get_object_or_404(SolicitudSinodal, pk=id)
            solicitud.fase = 3
            solicitud.estatus = 2
            solicitud.save()
            msg = 'Solicitud de sinodales enviada. Folio: ' + str(solicitud.id) + '. Estatus: Pendiente'
            notificacion = Notificaciones.objects.get(solicitud_id=id)
            notificacion.visto = False
            notificacion.descripcion = msg
            notificacion.fecha = timezone.now()
            notificacion.save()
            msgadmin = 'Nueva solicitud de sinodales de '+request.user.first_name+'. Folio: ' + str(solicitud.id)
            notificacionadmin = NotificacionAdmin(descripcion=msgadmin, fecha=timezone.now(), solicitud_id=solicitud.id, tipo_solicitud=2, nivel_educativo=solicitud.nivel_educativo)
            notificacionadmin.save()
            return redirect('SETyRS_detalle_solicitud_sinodal',id)
    else:
        raise Http404("El usuario no tiene permiso de ver esta página")

#Metodo que cambia el estado de la notificacion, redirige a la solicitud dependiendo si es de sinodal o de examenes
def leer_notificacion(request, id):
    notificacion=get_object_or_404(Notificaciones, pk=id)
    if notificacion.visto == False:
        notificacion.visto = True
        notificacion.save()
    if notificacion.tipo_solicitud == 1:
        return redirect('SETyRS_detalle_solicitud_examen', notificacion.solicitud_id)
    else:
        return redirect('SETyRS_detalle_solicitud_sinodal', notificacion.solicitud_id)


#VISTAS DE LA INSTITUCION EXAMENES A TITULO ------------------------------------------------------------------------------------------------

def guardar_Reglamento(request):
    centro =request.POST.get("centroTrabajo")
    #Obtenemos los files del POST
    files = request.FILES
    #Aislamos/separamos el archivo a guardar
    myfile = files['documentoPendiente']
    #Indicamos una ruta donde se almacenará el archivo
    fs = FileSystemStorage("media/SETyRS/archivos/reglamentos")
    #Hacemos el save del archivo indicando el nombre del archivo y el archivo como tal
    filename = fs.save(myfile.name, myfile)

    #Una vez guardamos el archivo en nuestro folder de media, guardamos la ruta del archivo en la bd
    reglamento = reglamento_interior_titulacion(CCT=centro, RIT="media/SETyRS/archivos/reglamentos/"+myfile.name)
    reglamento.save()
    return redirect('SETyRS_nueva_solicitud_examen')

def get_reglamento_titulacion(request):
    tieneReglamento = False
    try:
        RIT = reglamento_interior_titulacion.objects.filter(CCT=request.GET["cct"])
    except ObjectDoesNotExist:
        RIT= None
    return JsonResponse(serializers.serialize("json",RIT),safe=False)


def get_nivel_CCT(request):
    niveles = serializers.serialize("json",UsuarioInstitucion.objects.filter(cct=request.GET['cct']))
    return JsonResponse(niveles,safe=False)

def nueva_solicitud_examen(request):
    if request.user.tipo_usuario=='1' and request.user.tipo_persona=='2':
        centrosRegistrados = UsuarioInstitucion.objects.filter(id_usuariobase_id=request.user.id)
        notificacion = Notificaciones.objects.filter(user_id=request.user.id).order_by('-fecha')
        num_notifi = contarNotificaciones(request.user.id)
        sinodales = Sinodales.objects.filter(user_id=request.user.id, estatus=2).order_by('nombre_sinodal')
        context = {'notificacion':notificacion,'notificaciones':num_notifi,'sinodales':sinodales,'centrosRegistrados':centrosRegistrados}
        return render(request, 'institucion/sinodales/examenes/nueva_solicitud.html', context)
    else:
        raise Http404('El usuario no tiene permiso de ver esta página')

def detalle_solicitud_examen(request, id):
    if request.user.tipo_usuario=='1' and request.user.tipo_persona=='2':
        solicitud = get_object_or_404(SolicitudExamen, pk=id)
        if solicitud.user_id == request.user.id:
            notificacion = Notificaciones.objects.filter(user_id=request.user.id).order_by('-fecha')
            num_notifi = contarNotificaciones(request.user.id)
            lista_alumnos = Alumnos.objects.filter(id_solicitud_id=id).order_by('nombre_alumno')
            context = {'lista_alumnos': lista_alumnos, 'solicitud':solicitud,
                       'notificacion':notificacion,'notificaciones':num_notifi}
            if solicitud.fase == 1:
                return render(request, 'institucion/sinodales/examenes/agregar_alumnos.html', context)
            elif solicitud.fase == 2:
                archivos = ArchivosAlumnos.objects.filter(solicitud_id=id).order_by('id')
                context.update({'archivos':archivos})
                return render(request, 'institucion/sinodales/examenes/agregar_documentos_alumnos.html', context)
            else:
                if solicitud.estatus == 2:
                    solicitud.estatus = 'Pendiente'
                if solicitud.estatus == 3:
                    solicitud.estatus = 'Aprobada'
                if solicitud.estatus == 4:
                    solicitud.estatus = 'Rechazada'
                    historial_rechazo = get_object_or_404(Historial_admins_examen,solicitud_id=id)
                    context.update({'comentarios':historial_rechazo})
                archivos = ArchivosAlumnos.objects.filter(solicitud_id=id).order_by('id')
                presidente = get_object_or_404(Sinodales, pk=solicitud.id_presidente)
                secretario = get_object_or_404(Sinodales, pk=solicitud.id_secretario)
                vocal =  get_object_or_404(Sinodales, pk=solicitud.id_vocal)
                context.update({'p':presidente, 's':secretario, 'v':vocal, 'archivos':archivos})
                return render(request, 'institucion/sinodales/examenes/informacion_solicitud_examen.html', context)
        else:
            raise Http404("El usuario no tiene permiso de ver esta página")
    else:
        raise Http404('El usuario no tiene permiso de ver esta página')

def lista_solicitudes_examenes(request):
    if request.user.tipo_usuario=='1' and request.user.tipo_persona=='2':
        notificacion = Notificaciones.objects.filter(user_id=request.user.id).order_by('-fecha')
        num_notifi = contarNotificaciones(request.user.id)
        data = SolicitudExamen.objects.filter(user_id=request.user.id).order_by('-id')
        context = {"data":data,'notificacion':notificacion,'notificaciones':num_notifi}
        for s in data:
            c = s.categoria
            if c==1:
                s.categoria = 'SEMINARIO DE TITULACION'
            elif c==2:
                s.categoria = 'TESIS EXTERNA'
            elif c==3:
                s.categoria = 'INFORME SOBRE SERVICIO SOCIAL'
            elif c==4:
                s.categoria = 'ESTUDIOS DE POSGRADO'
            elif c==5:
                s.categoria = 'EXAMEN GENERAL DE CONOCIMIENTOS'
            elif c==6:
                s.categoria = 'EXAMEN CENEVAL'
            elif c==7:
                s.categoria = 'ALTO RENDIMIENTO DE LICENCIATURA'
            elif c==8:
                s.categoria = 'EXPERIENCIA PROFESIONAL'
            e = s.estatus
            if e==1:
                s.estatus = 'Incompleta'
            elif e==2:
                s.estatus = 'Pendiente'
            elif e==3:
                s.estatus = 'Aprobada'
            elif e==4:
                s.estatus = 'Rechazada'     
        return render(request, 'institucion/sinodales/examenes/lista_solicitudes_examenes.html', context)
    else:
        raise Http404('El usuario no tiene permiso de ver esta página')


# FUNCIONES DE LA INSTITUCION EXAMENES A TITULO------------------------------------------------------------------------------------------------

def crear_solicitud_examen(request):
    if request.user.tipo_usuario=='1' and request.user.tipo_persona=='2':
        if request.method == 'POST':
            categoria = request.POST["categoria"]
            presidente = request.POST["presidente"]
            secretario = request.POST["secretario"]
            cct = request.POST["cct"]
            vocal = request.POST["vocal"]
            escuela = CustomUser.objects.get(id=request.user.id)
            #if escuela.nivel_educativo == 3:
            nivel_educativo = request.POST['nivel']
            fecha_e = request.POST["fecha_exa"]
            lugar_e = request.POST["Lugar_exa"]
            hora_e = request.POST["hora_exa"]
            solicitud = SolicitudExamen(categoria=categoria, id_presidente=presidente, id_secretario=secretario, id_vocal=vocal, 
                                        institucion=escuela.id, user_id=request.user.id, fecha=date.today(), nivel_educativo=nivel_educativo,fecha_exa=fecha_e,lugar_exa=lugar_e,hora_exa=hora_e,CCT=cct)
            solicitud.save()
            msg = 'Nueva solicitud de exámenes a titulo. Folio: ' + str(solicitud.id) + '. Estatus: Incompleta'
            notificacion = Notificaciones(descripcion=msg, fecha=timezone.now(), solicitud_id=solicitud.id, tipo_solicitud=1, user_id=request.user.id)
            notificacion.save()
            return redirect('SETyRS_detalle_solicitud_examen', solicitud.id)
        else:
            return redirect('SETyRS_nueva_solicitud_examen')
    else:
        raise Http404('El usuario no tiene permiso de ver esta página')

def agregar_alumno(request, id):
    if request.user.tipo_usuario=='1' and request.user.tipo_persona=='2':
        if request.method == 'POST':
            nombre=request.POST["nombre"].upper()
            certificado=request.POST["certificado"].upper()
            curp=request.POST["curp"].upper()
            folio=request.POST["folio_pago"].upper()
            carrera=request.POST["carrera"].upper()
            alumno = Alumnos(no_certificado=certificado, nombre_alumno=nombre, CURP=curp, id_solicitud_id=id,folio_pago=folio,carrera=carrera)
            alumno.save()
            return redirect('SETyRS_detalle_solicitud_examen', id)
        else:
            return redirect('SETyRS_detalle_solicitud_examen', id)
    else:
        raise Http404('El usuario no tiene permiso de ver esta página')

def editar_alumno(request):
    if request.user.tipo_usuario=='1' and request.user.tipo_persona=='2':
        if request.method == 'POST':
            idAlumno = request.POST["idAlumn"]
            alumno = Alumnos.objects.get(pk=idAlumno)
            alumno.nombre_alumno = request.POST["nom"]
            alumno.no_certificado = request.POST["cert"]
            alumno.CURP = request.POST["curp"]
            alumno.folio_pago = request.POST["folio_pago"]
            alumno.save()
            solicitud = alumno.id_solicitud_id
            return redirect('SETyRS_detalle_solicitud_examen', solicitud)
        else:
            raise Http404('El usuario no tiene permiso de ver esta página')
    else:
        raise Http404('El usuario no tiene permiso de ver esta página')

def eliminar_alumno(request):
    if request.user.tipo_usuario=='1' and request.user.tipo_persona=='2':
        if request.method == 'POST':
            idAlumno = request.POST["idAl"]
            alumno = Alumnos.objects.get(pk=idAlumno)
            solicitud = alumno.id_solicitud_id
            alumno.delete()
            return redirect('SETyRS_detalle_solicitud_examen', solicitud)
        else:
            raise Http404('El usuario no tiene permiso de ver esta página')
    else:
        raise Http404('El usuario no tiene permiso de ver esta página')

def agregar_documentos_alumno(request, id):
    if request.user.tipo_usuario=='1' and request.user.tipo_persona=='2':
        if request.method == 'POST':
            solicitud = get_object_or_404(SolicitudExamen, pk=id)
            solicitud.fase = 2
            solicitud.save()
            return redirect('SETyRS_detalle_solicitud_examen', id)
        else:
            return redirect('SETyRS_detalle_solicitud_examen', id)
    else:
        raise Http404('El usuario no tiene permiso de ver esta página')

def subir_documentos_alumno(request, id):
    if request.user.tipo_usuario=='1' and request.user.tipo_persona=='2':
        if request.method == 'POST':
            form = ArchivosAlumnosForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
            else:
                error = 'Solo son validos los archivos PDF'
                messages.error(request, error)
            return redirect('SETyRS_detalle_solicitud_examen', id)
        else:
            return redirect('SETyRS_detalle_solicitud_examen', id)
    else:
        raise Http404('El usuario no tiene permiso de ver esta página')

def editar_documentos_alumno(request, id):
    if request.user.tipo_usuario=='1' and request.user.tipo_persona=='2':
        if request.method == 'POST':
            docs = ArchivosAlumnos.objects.get(alumno_id = request.POST['alumno'])
            if request.FILES:
                if 'certificado_egreso' in request.FILES:
                    docs.certificado_egreso.delete()
                    docs.certificado_egreso = request.FILES['certificado_egreso']
                if 'servicio_social' in request.FILES:
                    docs.servicio_social.delete()
                    docs.servicio_social = request.FILES['servicio_social']
                if 'inscripcion_ctrl_escolar' in request.FILES:
                    docs.inscripcion_ctrl_escolar.delete()
                    docs.inscripcion_ctrl_escolar = request.FILES['inscripcion_ctrl_escolar']
                if 'recibo_pago' in request.FILES:
                    docs.recibo_pago.delete()
                    docs.recibo_pago = request.FILES['recibo_pago']
                docs.save()
            return redirect('SETyRS_detalle_solicitud_examen', id)
        else:
            return redirect('SETyRS_detalle_solicitud_examen', id)
    else:
        raise Http404('El usuario no tiene permiso de ver esta página')

def finalizar_solicitud_examen(request, id):
    if request.user.tipo_usuario=='1' and request.user.tipo_persona=='2':
        if request.method == 'POST':
            solicitud = get_object_or_404(SolicitudExamen, pk=id)
            solicitud.fase = 3
            solicitud.estatus = 2
            solicitud.save()
            msg = 'Solicitud de exámenes a titulo enviada. Folio: ' + str(solicitud.id) + '. Estatus: Pendiente'
            notificacion = Notificaciones.objects.get(solicitud_id=id, tipo_solicitud=1)
            notificacion.visto = False
            notificacion.descripcion = msg
            notificacion.fecha = timezone.now()
            notificacion.save()
            msgadmin = 'Nueva solicitud de exámenes a título de '+request.user.first_name+'. Folio: ' + str(solicitud.id)
            notificacionadmin = NotificacionAdmin(descripcion=msgadmin, fecha=timezone.now(), solicitud_id=solicitud.id, tipo_solicitud=1,nivel_educativo=solicitud.nivel_educativo)
            notificacionadmin.save()
            return redirect('SETyRS_detalle_solicitud_examen', id)
        else:
            return redirect('SETyRS_detalle_solicitud_examen', id)
    else:
        raise Http404('El usuario no tiene permiso de ver esta página')

def generar_pdf(request, id):
    if  request.user.tipo_usuario=='1' or request.user.tipo_usuario=='2' or (request.user.tipo_usuario == '3' and request.user.departamento_id == 1):  #and request.user.tipo_persona=='2':
        solicitud = get_object_or_404(SolicitudExamen, pk=id)
        if solicitud.estatus == 3:
            h = Historial_admins_examen.objects.get(solicitud_id=solicitud.id)
            jefe = CustomUser.objects.get(id=h.user_id)
            params = {
                'solicitud': solicitud,
                'alumnos':Alumnos.objects.filter(id_solicitud_id=id), 
                'request': request,
                'escuela': UsuarioInstitucion.objects.get(cct=solicitud.CCT),
                'presidente': Sinodales.objects.get(id=solicitud.id_presidente),
                'secretario': Sinodales.objects.get(id=solicitud.id_secretario),
                'vocal': Sinodales.objects.get(id=solicitud.id_vocal),
                'jefe': jefe,
                'bucket': settings.MEDIA_URL
            }
            c = solicitud.categoria
            # Se hace la comparación en char porque la BD de producción tiene la columna categoria como varchar y no int
            if c=='1':
                solicitud.categoria = 'SEMINARIO DE TITULACION'
            elif c=='2':
                solicitud.categoria = 'TESIS EXTERNA'
            elif c=='3':
                solicitud.categoria = 'INFORME SOBRE SERVICIO SOCIAL'
            elif c=='4':
                solicitud.categoria = 'ESTUDIOS DE POSGRADO'
            elif c=='5':
                solicitud.categoria = 'EXAMEN GENERAL DE CONOCIMIENTOS'
            elif c=='6':
                solicitud.categoria = 'EXAMEN CENEVAL'
            elif c=='7':
                solicitud.categoria = 'ALTO RENDIMIENTO DE LICENCIATURA'
            elif c=='8':
                solicitud.categoria = 'EXPERIENCIA PROFESIONAL'
            elif c=='9':
                solicitud.categoria = 'OPCIÓN ESPECIFICADA POR LA INSTITUCIÓN'
            return Render.render('institucion/examenes/formato_aprobacion_solicitud.html', params)
        else:
             raise Http404("El usuario no tiene permiso de ver esta página")
    else:
         raise Http404("El usuario no tiene permiso de ver esta página")