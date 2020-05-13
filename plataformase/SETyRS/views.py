from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.utils import timezone
from datetime import date
from django.contrib import messages

from .models import *
from .forms import *
from RVOES.models import Departamento
from login.models import UsuarioInstitucion

# Vistas del administrador-----------------------------------------------------------------------------
# el departamento de dirección es el unico que puede ver e interactuar con las solicitudes de ambos niveles educativos (superior y media superior)
#dirección: 2
#superior: 3
#media superior: 4

# funcion que retorna el index del administrador con el contexto de acuerdo al departamento del usuario
def index_admin(request):
    #si el usuario no pertenece a cualquiera de estos 3 departamentos, se mostrará el error 404
    if request.user.departamento_id==2 or request.user.departamento_id==3 or request.user.departamento_id==4:
        dep = get_object_or_404(Departamento, pk=request.user.departamento_id)
        num_notifi = contarNotificacionesadmin(request.user.departamento_id) # cuenta las notificaciones que no han sido leidas y retorna el total
        if request.user.departamento_id == 2: #si el usuario pertenece al departamento DIRECCION
            notificacion = NotificacionAdmin.objects.filter().order_by('-fecha') #Recupera las notificaciones del administrador

        elif request.user.departamento_id == 3: #si el usuario pertenece al departamento SUPERIOR
            notificacion = NotificacionAdmin.objects.filter(nivel_educativo=2).order_by('-fecha') #Recupera las notificaciones del administrador

        elif request.user.departamento_id == 4: #si el usuario pertenece al departamento MEDIA SUPERIOR
            notificacion = NotificacionAdmin.objects.filter(nivel_educativo=1).order_by('-fecha') #Recupera las notificaciones del administrador
        
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


# Funciones del administrador-------------------------------------------------------------------------
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

# Vistas de la institución SINODALES-----------------------------------------------------------------------------
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
        notificacion = Notificaciones.objects.filter(user_id=request.user.id).order_by('-fecha')
        num_notifi = contarNotificaciones(request.user.id)
        context = {'notificacion':notificacion,'notificaciones':num_notifi}
        return render(request, 'institucion/sinodales/nueva_solicitud.html', context)
    else:
        raise Http404("El usuario no tiene permiso de ver esta página")

# funcion que retorna 3 plantillas diferentes de acuerdo a la fase o estatus en la que se encuentra la solicitud de sinodales
#Recibe el id de la solicitud
def detalle_solicitud_sinodal(request, id):
    if request.user.tipo_usuario=='1' and request.user.tipo_persona=='2':
        solicitud = get_object_or_404(SolicitudSinodal, pk=id)
        if solicitud.user_id == request.user.id:
            notificacion = Notificaciones.objects.filter(user_id=request.user.id).order_by('-fecha')
            num_notifi = contarNotificaciones(request.user.id)
            lista_sinodales = Sinodales.objects.filter(id_solicitud_id=id).order_by('nombre_sinodal')
            archivos = ArchivosSinodales.objects.filter(solicitud_id=id).order_by('id')
            context = {'lista_sinodales': lista_sinodales, 'solicitud':solicitud, 'archivos':archivos, 'notificacion':notificacion,'notificaciones':num_notifi}
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

# Funciones de la institución SINODALES--------------------------------------------------------------------------
# Metodo que retorna el total de notificaciones no leidas por el usuario. Recibe el id del usuario logueado
def contarNotificaciones(id):
    notificacion = Notificaciones.objects.filter(user_id=id, visto=False).count()
    return notificacion

# Metodo guarda una solcitud de sinodales en la BD
def crear_solicitud_sinodal(request):
    if request.user.tipo_usuario=='1' and request.user.tipo_persona=='2':
        if request.method == 'POST':
            user_id = request.user.id
            datos_escuela = get_object_or_404(UsuarioInstitucion, id_usuariobase_id=user_id)
            solicitud = SolicitudSinodal(user_id=user_id, fecha=timezone.now(), institucion=request.user.first_name,nivel_educativo=datos_escuela.nivel_educativo)
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
            comprobar_duplicidad = Sinodales.objects.filter(curp=curp, institucion=request.user.first_name)
            if comprobar_duplicidad:
                error = 'Este sinodal ya existe en su registro'
                messages.error(request, error)
                return redirect('SETyRS_detalle_solicitud_sinodal',id)
            else:
                datos_escuela = get_object_or_404(UsuarioInstitucion, id_usuariobase_id=request.user.id)
                sinodal = Sinodales(nivel_educativo=datos_escuela.nivel_educativo,nombre_sinodal=nombre, curp=curp, rfc=rfc,grado_academico=grado, id_solicitud_id=id, user_id=request.user.id, institucion=request.user.first_name)
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

#Vistas de la institucion EXAMENES A TITULO ------------------------------------------------------------------------------------------------
def nueva_solicitud_examen(request):
    if request.user.tipo_usuario=='1' and request.user.tipo_persona=='2':
        datos_escuela = UsuarioInstitucion.objects.get(id_usuariobase_id=request.user.id)
        nivel = datos_escuela.nivel_educativo
        notificacion = Notificaciones.objects.filter(user_id=request.user.id).order_by('-fecha')
        num_notifi = contarNotificaciones(request.user.id)
        sinodales = Sinodales.objects.filter(user_id=request.user.id, estatus=2).order_by('nombre_sinodal')
        context = {'notificacion':notificacion,'notificaciones':num_notifi,'sinodales':sinodales, 'nivel':nivel}
        return render(request, 'institucion/examenes/nueva_solicitud.html', context)
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
                return render(request, 'institucion/examenes/agregar_alumnos.html', context)
            elif solicitud.fase == 2:
                archivos = ArchivosAlumnos.objects.filter(solicitud_id=id).order_by('id')
                context.update({'archivos':archivos})
                return render(request, 'institucion/examenes/agregar_documentos.html', context)
            else:
                if solicitud.estatus == 2:
                    solicitud.estatus = 'Pendiente'
                if solicitud.estatus == 3:
                    solicitud.estatus = 'Aprobada'
                if solicitud.estatus == 4:
                    solicitud.estatus = 'Rechazada'
                    historial_rechazo = get_object_or_404(Historial_admins_examen,solicitud_id=id)
                    context.update({'comentarios':historial_rechazo})
                presidente = get_object_or_404(Sinodales, pk=solicitud.id_presidente)
                secretario = get_object_or_404(Sinodales, pk=solicitud.id_secretario)
                vocal =  get_object_or_404(Sinodales, pk=solicitud.id_vocal)
                context.update({'p':presidente, 's':secretario, 'v':vocal})
                return render(request, 'institucion/examenes/informacion_solicitud_examen.html', context)
        else:
            raise Http404("El usuario no tiene permiso de ver esta página")
    else:
        raise Http404('El usuario no tiene permiso de ver esta página')

#Funciones de la institucion EXAMENES A TITULO------------------------------------------------------------------------------------------------

def crear_solicitud_examen(request):
    if request.user.tipo_usuario=='1' and request.user.tipo_persona=='2':
        if request.method == 'POST':
            categoria = request.POST["categoria"]
            presidente = request.POST["presidente"]
            secretario = request.POST["secretario"]
            vocal = request.POST["vocal"]
            #escuela = UsuarioInstitucion.objects.get(id_usuariobase_id=request.user.id)
            #if escuela.nivel_educativo == 3:
            nivel_educativo = request.POST['nivel']
            solicitud = SolicitudExamen(categoria=categoria, id_presidente=presidente, id_secretario=secretario, id_vocal=vocal, 
                                        institucion_id=request.user.id, user_id=request.user.id, fecha=date.today(), nivel_educativo=nivel_educativo)
            solicitud.save()
            msg = 'Nueva solicitud de exámenes a titulo. Folio: ' + str(solicitud.id) + '. Estatus: Incompleta'
            notificacion = Notificaciones(descripcion=msg, fecha=timezone.now(), solicitud_id=solicitud.id, tipo_solicitud=1, user_id=request.user.id)
            notificacion.save()
            return redirect('SETyRS_detalle_solicitud_examen', solicitud.id)
        else:
            return redirect('SETyRS_nueva_solicitud_examen')
    else:
        raise Http404('El usuario no tiene permiso de ver esta pagina')