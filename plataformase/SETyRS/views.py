from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.utils import timezone
from datetime import date

from .models import *
from .forms import *
from RVOES.models import Departamento

# Vistas del administrador-----------------------------------------------------------------------------
# funcion que retorna el index del administrador con el contexto de acuerdo al departamento del usuario
def index_admin(request):
    if request.user.tipo_usuario=='2' or request.user.tipo_usuario=='3' or request.user.tipo_usuario=='4' and not request.user.is_superuser:
        usr = request.user
        dep = get_object_or_404(Departamento, pk=usr.departamento_id)
        if request.user.tipo_usuario=='2': #si el usuario pertenece al departamento DIRECCION
            notificacion = NotificacionAdmin.objects.filter().order_by('-fecha') #Recupera las notificaciones del administrador
            num_notifi = contarNotificacionesadmin(dep.id) # cuenta las notificaciones que no han sido leidas y retorna el total
            context = {'department':dep,'notificacion':notificacion,'notificaciones':num_notifi}
            return render(request,'admins/index_admin.html', context)

        elif request.user.tipo_usuario=='3': #si el usuario pertenece al departamento SUPERIOR
            return render(request,'admins/index_admin.html', None)

        elif request.user.tipo_usuario=='4': #si el usuario pertenece al departamento MEDIA SUPERIOR
            return render(request,'admins/index_admin.html', None)

    else:
        raise Http404("El usuario no tiene permiso de ver esta página")

# Vistas de la institución-----------------------------------------------------------------------------
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

# Funciones de la institución--------------------------------------------------------------------------
# Metodo que retorna el total de notificaciones no leidas por el usuario. Recibe el id del usuario logueado
def contarNotificaciones(id):
    notificacion = Notificaciones.objects.filter(user_id=id, visto=False).count()
    return notificacion

# Metodo guarda una solcitud de sinodales en la BD
def crear_solicitud_sinodal(request):
    if request.method == 'POST':
        user = request.user.id
        solicitud = SolicitudSinodal(user_id=user, fecha=timezone.now(), institucion=request.user.first_name)
        solicitud.save()
        msg = 'Nueva solicitud de sinodales. Folio: ' + str(solicitud.id) + '. Estatus: Incompleta'
        notificacion = Notificaciones(descripcion=msg, fecha=timezone.now(), solicitud_id=solicitud.id, tipo_solicitud=2, user_id=user)
        notificacion.save()
        return redirect('SETyRS_detalle_solicitud_sinodal', solicitud.id)
    else:
        return redirect('SETyRS_nueva_solicitud_sinodal')

# Metodo que agrega en la BD sinodales para la solicitud. Recibe el id de la solicitud 
def agregar_sinodal(request, id):
    if request.user.tipo_usuario=='1' and request.user.tipo_persona=='2':
        if request.method == 'POST':
            nombre=request.POST["nombre_sinodal"]
            curp=request.POST["curp"]
            rfc=request.POST["rfc"]
            grado=request.POST["grado_academico"]
            sinodal = Sinodales(nombre_sinodal=nombre, curp=curp, rfc=rfc,grado_academico=grado, id_solicitud_id=id, user_id=request.user.id)
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
            solicitud.fase += 1
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
            solicitud.fase += 1
            solicitud.estatus += 1
            solicitud.save()
            msg = 'Solicitud de sinodales enviada. Folio: ' + str(solicitud.id) + '. Estatus: Pendiente'
            notificacion = Notificaciones.objects.get(solicitud_id=id)
            notificacion.visto = False
            notificacion.descripcion = msg
            notificacion.fecha = timezone.now()
            notificacion.save()
            msgadmin = 'Nueva solicitud de sinodales. Folio: ' + str(solicitud.id)
            notificacionadmin = NotificacionAdmin(descripcion=msgadmin, fecha=timezone.now(), solicitud_id=solicitud.id, tipo_solicitud=2)
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

# Funciones del administrador-------------------------------------------------------------------------
# Metodo que retorna el total de notificaciones que no han sido leidas dependiendo del departamento del usuario activo
def contarNotificacionesadmin(departamento):
    if departamento=='2':
        notificacion = NotificacionAdmin.objects.filter(visto=False).count()
        return notificacion
    elif departamento=='3':
        notificacion = NotificacionAdmin.objects.filter(visto=False, departamento_id=departamento).count()
        return notificacion
    elif departamento=='4':
        notificacion = NotificacionAdmin.objects.filter(visto=False, Departamento_id=departamento).count()
        return notificacion