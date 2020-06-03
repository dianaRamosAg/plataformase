from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.views.generic.base import View
from .models import *
from login.models import CustomUser, UsuarioInstitucion
from django.db.models.expressions import RawSQL
from .forms import *
from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string

from django.views.generic import View
from django.utils import timezone
from .models import *
from .render import render_pdf_planes_prog_estud

"""
Todos los métodos (menos class Pdf(View)) incluyen el siguiente código:
#Si el tipo de usuario que hizo la solicitud es (1: institución, 2-3: personal del departamento)
if request.user.tipo_usuario == '1'or request.user.tipo_usuario == '5':
    #Código del método
    ...
#Si no corresponde el tipo de usuario lo manda a su página principal o login por defecto
else:
    return redirect('perfil')
"""

class Pdf(View):
    """
    Clase utilizada para generar un archivo PDF sobre el documento de "Revisión de Planes y Programas de Estudio".
    Esta clase utiliza un método que viene del archivo "render.py" llamado "render_pdf_planes_prog_estud".
    """
    def get(self, request, id):
        """Parámetros
        -:param request: Contiene información del navegador del usuario que está realizando la petición.
        -:param id: Es el id de la solicitud para saber sobre que solicitud se va a generar el archivo PDF

        Retorna
        -:return: Regresa el pdf de planes y programas de estudio.
        """
        return render_pdf_planes_prog_estud(request, id)

def index_user(request):
    """
    Este método manda a llamar la plantilla "Inicio.html" como pantalla principal al momento de que el usuario
    'institución' inicie sesión.
    'TotalNotificaciones' es una variable que almacena el resultado de un QuerySet que cuenta los registros
    (que simulan notificaciones) de tipo "Historial" pertenecientes al usuario, que no han sido leídas (leida=0). Esta
    variable es enviada a plantilla para su mostrar su valor dentro de la plantilla.

    Parámetros
    -:param request: Contiene información del navegador del usuario que está realizando la petición.

    Retorna
    -:return: Regresa la plantilla "Inicio.html" (página principal del usuario).
    """
    if request.user.tipo_usuario == '1' or request.user.tipo_usuario == '5' :
        TotalNotificaciones = Notificacion.objects.filter(leida='0', tipo_notificacion='H',
                                                        usuario_id=request.user.id).count()
        return render(request, 'Inicio.html', {"total": TotalNotificaciones})
    else:
        return redirect('perfil')

def acuerdos(request):
    """
    Manda a llamar la plantilla "acuerdos.html" para que las instituciones puedan saber cuales son los acuerdos
    correspondientes a su nivel. Estos acuerdos son subidos por el admnistrador del sistema.
    La variable docsMS obtiene todos los acuerdos correspondientes al nivel Media Superior (1).
    La variable docsS obtiene todos los acuerdos correspondientes al nivel Superior (2).

    Parámetros
    -:param request: Contiene información del navegador del usuario que está realizando la petición.

    Retorna
    -:return: Regresa la plantilla "acuerdos.html" en la cual la institución visualiza los acuerdos para realizar una
    solicitud de RVOE
    """
    if request.user.tipo_usuario == '1' or request.user.tipo_usuario == '5':
        docsMS = Acuerdos.objects.filter(nivel='1')#Obtiene los acuerdos correspondientes para Media Superior.
        docsS = Acuerdos.objects.filter(nivel='2')#Obtiene los acuerdos correspondientes para Superior.
        return render(request, 'acuerdos.html', {'docsMS': docsMS, 'docsS': docsS})
    else:
        return redirect('perfil')

def validacion(request):
    """
    Este método verifica si existe alguna solicitud con archivos pendidientes por subir.
    La variable "record" obtiene el "id" de la última solicitud ingresada al sistema por el usuario y el valor
    "completado" para definir en que carpeta quedó la solicitud (Carpetas: -1 = Cancelada, 0 = Completado, 1 = Institucional,
    2 = Curricular, 3 = Académica, 4 = Media Superior, 10 = Documentos recibidos, 11 = Terminó revisión digital).
    De existir alguna solicitud pendiente, le informa a la institución, mediante la plantilla "faltaArchivos.html",
    para que decida si quiere continuar con esa solicitud o si quiere comenzar una nueva. De no existir alguna
    solicitud  pendiente, redirige al usuario a la URL con llamada "solicitud".

    Parámetros
    -:param request: Contiene información del navegador del usuario que está realizando la petición.

    Retorna
    -:return redirect: Redirige a la página solicitud.
    -:return render: Retorna la plantilla "faltaArchivos.html" para preguntar a la institución si quiere continuar con la
     solicitud pendiente o empezar una nueva.
    """
    if request.user.tipo_usuario == '1' or request.user.tipo_usuario == '5':
        record = Solicitud.objects.values_list('completado', 'id').filter(customuser=request.user.id).last()
        if not record == None:#Si no existe una solicitud ingresada
            if (record[0] != 11) and (record[0] != 10):#Si la última solicitud aún no a terminado su revición digital
                if record:
                    if record[0] == 0 or record[0] == -1:#Si la última solicitud esta completada o esta cancelada
                        return redirect('solicitud')#Redirecciona al usuario a la URL llamada "solicitud"
                    else:
                        if record[0] >= 1 or record[0] <= 4: #Si la solicitud se encuentra pendiente de archivos e cualquier carpeta
                            return render(request, 'faltaArchivos.html',
                                        {"carpeta": record[0],
                                        "folio": record[1], })#Llama la plantilla "faltaArchivos.html" y le manda los
                                                        #valores de as variables id de solicitud e id de carpeta n la que se encuentra
                        else:
                            return redirect('solicitud')#Redirecciona al usuario a la URL llamada "solicitud"
        return redirect('solicitud')#Redirecciona al usuario a la URL llamada "solicitud"
    else:
        return redirect('perfil')

def solicitud(request):
    """
    Método que llama la plantilla "solicitud.html" la cual inicia el proceso de turno para una Solicitud de RVOE.
    En este método, también elimina la última solicitud, solo si esta fue cancelada por la propia institución, cuando el
    proceso quedó pendiente de subida de archivos.
    La variable "record" obtiene el "id" de la última solicitud ingresada al sistema por el usuario y el valor
    "completado" para definir en qué carpeta quedo la solicitud (Carpetas: -1 = Cancelada, 0 = Completado, 1 = Institucional,
    2 = Curricular, 3 = Académica, 4 = Media Superior, 11 = Terminó revisión digital).

    Parámetros
    -:param request: Contiene información del navegador del usuario que está realizando la petición.

    Retorna
    -:return: Retorna la plantilla "solicitud.html" para que el usuario empiece el proceso de solicitud de RVOE.
    """
    if request.user.tipo_usuario == '1'or request.user.tipo_usuario == '5':
        #record obtiene de la última solicitud del usuario, el valor de los campos "completado" e "id"
        record = Solicitud.objects.values_list('completado', 'id').filter(customuser=request.user.id).last()
        if record:#Si se obtuvo algún resultado
            if record[1] != -1:#Si el id es diferente a -1 (Posible borrado de esta línea)
                if record[0] >= 1 and record[0] <= 4:#Si la solicitud se encuentra pediente en alguna carpeta
                    Solicitud.objects.filter(id=record[1]).delete()#Borra la solicitud de la base de datos.
        cct = UsuarioInstitucion.objects.filter(id_usuariobase=request.user.id)
        return render(request, 'solicitud.html', {'cct': cct})#Llama a la plantilla de "solicitud.html" para que el usuario la visualice.
    else:
        return redirect('perfil')

def solicitud_insert(request):
    """
    En este método se inserta la solicitud en la base de datos, con la información obtenida de la plantilla "solicitud.html".
    Si la informaion viene en un request con método de envío de datos diferente a POST, redirecciona a la URL con con el
    nombre "solicitd". Si la información se recibe con el método POST, entonces se guarda en la base de datos y según el
    nivel de la solicitud se le redirge a la URL especifica, si nivel = 1: Media Superior, nivel = 2: Superior.

    Parámetros
    -:param request: Contiene información del navegador del usuario que está realizando la petición.

    Retorna
    -:return redirect('medSuperior'): Redirige a la URL de Media Superior para que la institución pueda subir los archivos correspondientes.
    -:return redirect('institucionalSup'): Redirige a la URL de Superior para que la institución pueda subir los archivos correspondientes.
    -:return redirect('solicitud'): Redirige a la URL de Solicitud para que la institución pueda iniciar una nueva solicitud.
    """
    if request.user.tipo_usuario == '1'or request.user.tipo_usuario == '5':
        #Si el request es con el método POST, registra la solicitud en la base de datos y después lo redirige a subir archivos
        if request.method == 'POST':#Si el request fue realizada con el método POST
            import datetime#Librería para guardar la fecha
            #Según los datos introducidos en "solicitud.html" y enviados por el método POST se guardan en una variable
            nivel = request.POST["nivel"]
            modalidad = request.POST["modalidad"]
            opcion = request.POST["opcion"]
            salud = str(request.POST["salud"])
            customuser_id = (request.user.id)
            noInstrumentoNotarial = request.POST["noInstrumentoNotarial"]
            nombreNotario = request.POST["nombreNotario"]
            noNotario = request.POST["noNotario"]
            nombreRepresentante = request.POST["nombreRepresentante"]
            nombreSolicitud = request.POST["nombreSolicitud"]
            fechaRegistro = datetime.datetime.now()#Obtenemos la fecha actual
            estatus = Departamento.objects.get(id=2)#Obtenemos el primer departamento al que debe pasar
            #Si tipo de usuario es institución guarda la clave de centro de trabajo, de lo contrario no es necesario
            if request.user.tipo_usuario == '1':
                cct = request.POST["cct"]
            else:
                cct = None
            # Se generá la plantilla para inserción de solicitud
            solicitud = Solicitud(nivel=nivel, modalidad=modalidad, opcion=opcion,
                                salud=salud, customuser_id=customuser_id,
                                fechaRegistro=fechaRegistro, estatus=estatus,
                                noInstrumentoNotarial=noInstrumentoNotarial,
                                nombreNotario=nombreNotario, noNotario=noNotario,
                                nombreRepresentante=nombreRepresentante,
                                nombreSolicitud=nombreSolicitud, cct=cct)
            solicitud.save()#Guarda la solicitud
            if nivel == '1':#Si el nivel es uno, redirecciona a la URL para subir archivos de solicitudes de media superior
                return redirect('medSuperior')
            else:#Si el nivel no es uno, redirecciona a la URL para subir archivos de solicitudes de superior
                return redirect('institucionalSup')
        else:#Si el request no es con el método POST, redirige a la URL con nombre "Solicitud"
            return redirect('solicitud')
    else:
        return redirect('perfil')

def SInstitucional(request):
    """
    Este método almacena los documentos que han sido cargados en la plantilla "institucionalSup.html", esta plantilla pide
    a la institución todos los archivos correspondientes a la carpeta Institucional. Además este método actualiza el estado
    de en que carpeta se encuentra subiendo archivos actualmente (Carpeta Institucional [completado=1]).

    Parámetros
    -:param request: Contiene información del navegador del usuario que está realizando la petición.

    Retorna
    -:return: Retorna la plantilla "institucionalSup.html" para que la institución pueda subir los archivos correspondientes
     a la carpeta institucional.
    """
    if request.user.tipo_usuario == '1'or request.user.tipo_usuario == '5':
        request.POST._mutable = True#Activando esta opción podremos editar los datos que vienen del método POST
        request.POST["id_solicitud"] = Solicitud.objects.values_list('id').order_by('id').last()[0]#Pasamos el id de la solicitud en caso
        id_solicitud = Solicitud.objects.values_list('id').order_by('id').last()[0]#Es solo para inicializar el valor ya que el uso de la misma lo exige
        if request.method == 'POST':#Si el request fue realizado con el método POST
            '''
            #Se hace una consulta sobre si existe el número de folio de pago ya ingresado en el sistema
            folioPago = CMedSuperior.objects.filter(folio_pago=request.POST["folio_pago"]).exists()
            if folioPago:#Si existe, se borra para marcar que el folio es inválido, ya que este no se puede repetir.
                request.POST["folio_pago"] = None
                print("pago existe")
            '''
            form = ArchivosInstForm(request.POST, request.FILES)#Se añaden los archivos y los campos de texto ingresados al sistema
            if form.is_valid():#Si el formulario es válido, lo guarda en la base de datos y redirige a la siguiente vista para que guarde los archivos de la siguente carpeta
                print("formulario valido")
                form.save()
                return redirect('curricularSup')#Redirige a la URL con nombre "curricularSup"
            print("formulario no valido")
        else:#Si el request no fue realizado con el método POST
            form = ArchivosInstForm()#Se crea el formulario de la información requerida según el modelo "CInstitucional"
            id_solicitud = Solicitud.objects.values_list('id').order_by('id').last()[0]#Se obtiene el ID de la ultima solicitud ingresada.
            Solicitud.objects.filter(id=id_solicitud).update(completado=1)#Actualiza en que carpeta se encuentra el proceso de subida de solicitud.
        from datetime import datetime
        fecha = datetime.today().strftime('%Y-%m-%d')
        return render(request, 'institucionalSup.html',
                    {'form': form,
                    'fecha': fecha,
                    "id_solicitud": Solicitud.objects.values_list('id').order_by('id').last()[0], })#Le muestra la plantilla "institucionalSup.html" al usuario y se le mandan las variables form e id solicitud.
    else:
        return redirect('perfil')

def SCurricular(request):
    """
    Este método almacena los documentos que han sido cargados en la plantilla "curricularSup.html", esta plantilla pide
    a la institución todos los archivos correspondientes a la carpeta Curricular. Además este método actualiza el estado
    de en que carpeta se encuentra subiendo archivos actualmente (Carpeta Curricular [completado=2]).

    Parámetros
    -:param request: Contiene información del navegador del usuario que está realizando la petición.

    Retorna
    -:return: Retorna la plantilla "curricularSup.html" para que la institución  pueda subir los archivos correspondientes
     a la carpeta curricular.
    """
    if request.user.tipo_usuario == '1'or request.user.tipo_usuario == '5':
        request.POST._mutable = True#Activando esta opción podremos editar los datos que vienen del método POST
        id_solicitud = Solicitud.objects.values_list('id').order_by('id').last()[0]
        request.POST["id_solicitud"] = id_solicitud#Pasamos el id de la solicitud en caso
        #id_solicitud = getUltSolicitud(request.user.id)#Es solo para inicializar el valor ya que el uso de la misma lo exige
        if request.method == 'POST':#Si el request fue realizado con el método POST
            form = ArchivosCCurrForm(request.POST, request.FILES)#Se añaden los archivos y los campos de texto ingresados al sistema
            if form.is_valid():#Si el formulario es válido, lo guarda en la base de datos y redirige a la siguiente vista para que guarde los archivos de la siguente carpeta
                form.save()
                return redirect('academicaSup')#Redirige a la URL con nombre "academicaSup"
        else:#Si el request no fue realizado con el método POST
            form = ArchivosCCurrForm()#Se crea el formulario de la información requerida según el modelo "CCurricular"
            id_solicitud = Solicitud.objects.values_list('id').order_by('id').last()[0]#Se obtiene el ID de la última solicitud ingresada.
            mod = Solicitud.objects.values_list('modalidad').get(id=id_solicitud)[0]#Se obtiene la modalidad de la última solicitud ingresada.
            salud = Solicitud.objects.values_list('salud').get(id=id_solicitud)[0]#Se obtiene de la última solicitud ingresada, si esta es pertenecienete al área de salud o no.
            Solicitud.objects.filter(id=id_solicitud).update(completado=2)#Actualiza en qué carpeta se encuentra el proceso de subida de solicitud.
        return render(request, 'curricularSup.html',
                    {'form': form, "id_solicitud": id_solicitud,
                    'mod': mod, 'salud': salud})#Le muestra la plantilla "curricularSup.html" al usuario y se le mandan las variables 'form', 'id solicitud', 'mod' y 'salud'.
    else:
        return redirect('perfil')

def SAcademica(request):
    """
    Este método almacena los documentos que han sido cargados en la plantilla "academicaSup.html", esta plantilla pide
    a la institución todos los archivos correspondientes a la carpeta Academica. Además este método actualiza el estado
    de en que carpeta se encuentra subiendo archivos actualmente (Carpeta Académica [completado=3]).

    Parámetros
    -:param request: Contiene información del navegador del usuario que está realizando la petición.

    Retorna
    -:return: Retorna la plantilla "academicaSup.html" para que la institución  pueda subir los archivos correspondientes
     a la carpeta académica.
    """
    if request.user.tipo_usuario == '1'or request.user.tipo_usuario == '5':
        request.POST._mutable = True#Activando esta opción podremos editar los datos que vienen del método POST
        request.POST["id_solicitud"] = Solicitud.objects.values_list('id').order_by('id').last()[0]#Pasamos el id de la solicitud en caso
        id_solicitud = Solicitud.objects.values_list('id').order_by('id').last()[0]#Es solo para inicializar el valor ya que el uso de la misma lo exige
        if request.method == 'POST':#Si el request fue realizado con el método POST
            form = ArchivosCAcadForm(request.POST, request.FILES)#Se añaden los archivos y los campos de texto ingresados al sistema
            if form.is_valid():#Si el formulario es válido, lo guarda en la base de datos y redirige a la siguiente vista para mostrarle el número de seguimiento de esa solicitud que es su ID
                form.save()
                return redirect('finSolicitud')#Redirige a la URL con nombre "finSolicitud"
        else:#Si el request no fue realizado con el método POST
            form = ArchivosCAcadForm()#Se crea el formulario de la información requerida según el modelo "CAcademica"
            id_solicitud = Solicitud.objects.values_list('id').order_by('id').last()[0]#Se obtiene el ID de la última solicitud ingresada.
            Solicitud.objects.filter(id=id_solicitud).update(completado=3)#Actualiza en que carpeta se encuentra el proceso de subida de solicitud.
        return render(request, 'academicaSup.html',
                    {'form': form,
                    "id_solicitud": id_solicitud, })#Le muestra la plantilla "academicaSup.html" al usuario y se le mandan las variables 'form' e 'id solicitud'.
    else:
        return redirect('perfil')

def SMedSuperior(request):
    """
    Este método almacena los documentos que han sido cargados en la plantilla "medSuperior.html", esta plantilla pide
    a la institución todos los archivos correspondientes a la carpeta única de Media Superior. Además este método actualiza
    el estado de en que carpeta se encuentra subiendo archivos actualmente (Carpeta Media Superior [completado=4]).

    Parámetros
    -:param request: Contiene información del navegador del usuario que está realizando la petición.

    Retorna
    -:return: Retorna la plantilla "medSuperior.html" para que la institución pueda subir los archivos correspondientes a la
     carpeta de media superior.
    """
    if request.user.tipo_usuario == '1'or request.user.tipo_usuario == '5':
        id_solicitud = Solicitud.objects.values_list('id').order_by('id').last()[0]#Es solo para inicializar el valor ya que el uso de la misma lo exige
        salud = Solicitud.objects.values_list('salud').get(id=id_solicitud)[0]#Obtiene si la solicitud pertenece al área de la salud
        virtual = Solicitud.objects.values_list('opcion').get(id=id_solicitud)[0]#Obtiene la opción a la que pertence la solicitud
        mod = Solicitud.objects.values_list('modalidad').get(id=id_solicitud)[0]#Obtiene la modalidad a la que pertence la solicitud
        request.POST._mutable = True#Activando esta opción podremos editar los datos que vienen del método POST
        request.POST["id_solicitud"] = Solicitud.objects.values_list('id').order_by('id').last()[0]#Pasamos el id de la solicitud en caso
        if request.method == 'POST':#Si el request fue realizado con el método POST
            form = ArchivosMedSupForm(request.POST, request.FILES)#Se añaden los archivos y los campos de texto ingresados al sistema
            if form.is_valid():#Si el formulario es válido, lo guarda en la base de datos y redirige a la siguiente vista para mostrarle el número de seguimiento de esa solicitud que es su ID
                form.save()
                return redirect('finSolicitud')#Redirige a la URL con nombre "finSolicitud"
        else:
            form = ArchivosMedSupForm()#Se crea el formulario de la información requerida según el modelo "CMedSuperior"
            Solicitud.objects.filter(id=id_solicitud).update(completado='4')#Actualiza en que carpeta se encuentra el proceso de subida de solicitud.
        from datetime import datetime
        fecha = datetime.today().strftime('%Y-%m-%d')
        return render(request, 'medSuperior.html',
                    {'form': form,
                    "id_solicitud": id_solicitud,
                    'fecha': fecha,
                    'virtual': virtual,
                    'mod': mod,
                    'salud': salud,})#Le muestra la plantilla "medSuperior.html" al usuario y se le mandan las variables 'form', 'salud' e 'id solicitud'.
    else:
        return redirect('perfil')

def finSolicitud(request):
    """
    Este método finaliza la subida de archivos poniendo en "0" el campo "completado" de la tabla "solicitud".
    Posteriormente notifica a todos los usuarios administrativos (jefes departamento y subordinados) que se ha ingresado
    una nueva solicitud y a la vez se le informa al usuario 'institución' que su solicitud se ha registrado.
    Finalmente se le muestra la plantilla "finSolicitud.html" la cual le dice cuál es el folio de seguimiento de esa
    solicitud.

    Parámetros
    -:param request: Contiene información del navegador del usuario que está realizando la petición.

    Retorna
    -:return: Retorna la plantilla "finSolicitud.html" para decirle a la institución que ahí acaba el proceso de subida de
     archivos y comienza el proceso de revisión.
    """
    if request.user.tipo_usuario == '1'or request.user.tipo_usuario == '5':
        import datetime#Se utiliza para obtener la fecha actual
        from django.db.models import Q#Se utiliza para hacer consultas más complejas con QuerySet
        id_solicitud = Solicitud.objects.values_list('id').order_by('id').last()[0]#Se obtiene la última solicitud ingresada por el usuario
        Solicitud.objects.filter(id=id_solicitud).update(completado=0)#Actualiza completado a 0 para decir que ya se encuentra completo de archivos.
        usuariosAdmin = CustomUser.objects.filter(Q(tipo_usuario=2) | Q(tipo_usuario=3))#Consulta de usuarios que son tipo 2 y 3 (jefe departamento y subordinados)
        for element in usuariosAdmin:
            notificacionA = Notificacion(solicitud_id=id_solicitud,
                                        descripcion="Nueva solicitud ingresada",
                                        leida='0',
                                        fechaNotificacion=datetime.datetime.now(),
                                        tipo_notificacion='P',
                                        usuario_id=element.id)#Plantilla de notificación para personal (jefes departamento y subordinados)
            notificacionA.save()#Guarda registro de notificación en la base de datos
        notificacionU = Notificacion(solicitud_id=id_solicitud,
                                    descripcion="Tu solicitud ha sido ingresada al sistema",
                                    leida='0',
                                    fechaNotificacion=datetime.datetime.now(),
                                    tipo_notificacion='H',
                                    usuario_id=request.user.id)#Plantilla de notificación para la institución
        notificacionU.save()#Guarda registro de la notificación en la base de datos
        return render(request, 'finSolicitud.html', {"id_solicitud": id_solicitud, })#Le muestra la plantilla "finSolicitud.html" a la institución.
    else:
        return redirect('perfil')

def estatus(request, usuario, solicitud):
    """Muestra al usuario 'institución' todas las solicitudes que ha realizado. También sirve para mostrar una solicitud
     específica pasando como parámetro de búsqueda su ID.

    Parámetros
    -:param request: Contiene información del navegador del usuario que está realizando la petición.
    -:param usuario: Se recibe el id del usuario mediante la URL
    -:param solicitud: Determina el tipo de solicitudes a mostrar, si soliciutd = "G": Muestra todas las solicitudes de ese
         usuario. Si solicitud = X(Cualquier otro número), muestra solo la solicitud que tenga ID = X.

    Retorna
    -:return: Regresa la vista en la cual el usuario podrá observar solicitudes que ha ingresado anteriormente.
    """
    if request.user.tipo_usuario == '1'or request.user.tipo_usuario == '5':
        try:
            if (solicitud == 'G'):# Si el parámetro 'solicitud' es una "G"
                Solicitudes = Solicitud.objects.filter(customuser=usuario).order_by('id')# Obtenemos todas las solicitudes pertenecientes a ese usuario.
            else: # Si es un número
                Solicitudes = Solicitud.objects.filter(id=solicitud, customuser=usuario, completado=0).order_by('id')# Obtenemos la solicitud perteneciente a ese usuario con la 'id de solicitud' dada.
            TotalNotificaciones = Notificacion.objects.filter(leida='0', tipo_notificacion='H',
                                                            usuario_id=request.user.id).count()#Obtenemos la cuenta de los registros (que simulan notificaciones) de tipo "Historial" pertenecientes al usuario, que no han sido leídas (leída=0).
        except Solicitud.DoesNotExist:
            raise Http404("Ningúna solicitud coincide con la consulta dada.")
        return render(request, 'estadoSolicitud.html', {"solicitudes": Solicitudes, "total": TotalNotificaciones})
    else:
        return redirect('perfil')

def historial(request, usuario, solicitud):
    """Muestra a la institución información más detallada de la solicitud que ha seleccionado,
     a través de un par de tablas que muestran el historial de notificaciones realizadas a esa
     solicitud y todos las observaciones a los documentos subidos a la misma.

    Parámetros
    -:param request: Contiene información del navegador del usuario que está realizando la petición.
    -:param usuario: Se recibe el id del usuario mediante la URL
    -:param solicitud: ID de la solicitud a consultar.

    Retorna
    -:return: Regresa la vista en la cual el usuario podrá observar información del proceso de la solicitud
    """
    if request.user.tipo_usuario == '1'or request.user.tipo_usuario == '5':
        try:
            comentario = Solicitud.objects.values_list("comentario").get(id=solicitud)[0]# Variable que nos permite determinar si la solicitud tiene comentarios o no.(0: no tiene comentarios, 1: si tiene comentarios)
            rechazada = Solicitud.objects.values_list("completado").get(id=solicitud)[0]# Variable que nos permite determinar si la solicitud ya fue rechazada(0: aún está vigente, 1: fue rechazada)
            Notificaciones = Notificacion.objects.filter(solicitud_id=solicitud, tipo_notificacion='H').order_by('id')# Se obtienen todas las notificaciones a esa solicitud de tipo 'Historial'(H).
            ComentariosSolic = Comentarios.objects.filter(solicitud_id=solicitud, mostrado=1)# Se obtienen todos los comentarios realizados a esta solicitud.
            medSup = CMedSuperior.objects.filter(id_solicitud=solicitud)#Obtenemos todos los archivos subidos en la carpeta media superior corespondientes a la solicitud
            cInst = CAcademica.objects.filter(id_solicitud=solicitud)#Obtenemos todos los archivos subidos en la carpeta institucional corespondientes a la solicitud
        except Notificacion.DoesNotExist:
            raise Http404("Ningúna Notificación coincide con la consulta dada.")
        return render(request, 'historialSolicitud.html', {"notificaciones": Notificaciones,
                                                        "comentarios": ComentariosSolic,
                                                        "solicitud": solicitud,
                                                        "comentario": comentario,
                                                        "rechazada": rechazada,
                                                        "medSup": medSup,
                                                        "cInst": cInst})
    else:
        return redirect('perfil')

def notificacionUsuario(request):
    """Muestra al usuario las notificaciones que tiene como no leídas.

    Parámetros
    -:param request: Contiene información del navegador del usuario que está realizando la petición.

    Retorna
    -:return: Regresa la vista en la cual el usuario podrá revisar las notificaciones que tiene que no han sido leídas.
    """
    if request.user.tipo_usuario == '1'or request.user.tipo_usuario == '5':
        import pickle # Importa una librería que nos permite la manipulación del acceso a memoria de una manera mas directa.
        Notificaciones = Notificacion.objects.filter(leida='0', tipo_notificacion='H', usuario_id=request.user.id).order_by(
            'fechaNotificacion')# Se obtienen todas las notificaciones no leídas (leida=0) de tipo 'Historial'(H) del usuario en sesión.
        s = pickle.dumps(Notificaciones)#Ponemos en memoria lo almacenado en 'Notificaciones' y almacenamos en 's' la referencia a estos datos.
        Notificacion.objects.filter(usuario_id=request.user.id, leida='0').update(leida='1')# Actualizamos las notificaciones no leídas del usuario, de "leida='0'" a "leida='1'", lo que se interpreta como que las mismas ya fueron leídas.
        NotificacionesAuxiliar = pickle.loads(s)# Almacenamos en 'NotificacionesAuxiliar' lo referenciado por 's'.
        return render(request, 'notificacionUsuario.html', {"notificaciones": NotificacionesAuxiliar})
    else:
        return redirect('perfil')

def historialNotificacionesUsuario(request):
    """Muestra al usuario todas las notificaciones que ha recibido.

    Parámetros
    -:param request: Contiene información del navegador del usuario que está realizando la petición.

    Retorna
    -:return: Regresa la vista en la cual el usuario podrá revisar todas las notificaciones que ha recibido.
    """
    if request.user.tipo_usuario == '1'or request.user.tipo_usuario == '5':
        Notificaciones = Notificacion.objects.filter(tipo_notificacion='H', usuario_id=request.user.id).order_by(
            'fechaNotificacion')# Se obtienen todas las notificaciones de tipo 'Historial'(H) del usuario en sesión.
        TotalNotificaciones = Notificacion.objects.filter(leida='0', tipo_notificacion='H',
                                                        usuario_id=request.user.id).count()#Se obtiene el total de notificaciones de tipo 'Historial' del usuario en sesión que no han sido leídas (leida='0').
        return render(request, 'notificacionUsuarioHistorial.html',
                    {"notificaciones": Notificaciones, "total": TotalNotificaciones})# Regresa la plantilla "notificacionUsuarioHistorial.html, donde se muestra al usuario todas las notificaciones que ha recibido"
    else:
        return redirect('perfil')

def verArchivos(request, usuario, solicitud):
    """Muestra al usuario los archivos subidos a la solicitud seleccionada.

    Parámetros
    -:param request: Contiene información del navegador del usuario que está realizando la petición.
    -:param usuario: Contiene el ID del usuario que está hacinedo la consulta.
    -:param solicitud: Contiene el ID de la solicitud que se ha seleccionado para ver sus archivos.

    Retorna
    -:return: Regresa la vista en la cual el usuario podrá ver los documentos subidos ordenados por carpeta.
    """
    if request.user.tipo_usuario == '1'or request.user.tipo_usuario == '5':
        tipoS = Solicitud.objects.values_list('nivel').get(id=solicitud)#Obtenemos si la solicitud es de nivel superior o nivel media superior
        #Inicialización de variables.
        if tipoS[0] == '1':#Si la solicitud es de Media Superior
            medSup = CMedSuperior.objects.filter(id_solicitud=solicitud)#Obtiene las rutas de los archivos de la carpeta de media superior.
            return render(request, 'archivosSolicitud.html',
                        {'medSup': medSup, 'folio': solicitud})#Regresa la plantilla "archivosSolicitud.html" para que el usuario vea los archivos subidos.
        else:#Si la solicitud es de Superior
            cInst = CInstitucional.objects.filter(id_solicitud=solicitud)#Obtiene las rutas de los archivos de la carpeta de institucional.
            cAcad = CAcademica.objects.filter(id_solicitud=solicitud)#Obtiene las rutas de los archivos de la carpeta de académica.
            cCurri = CCurricular.objects.filter(id_solicitud=solicitud)#Obtiene las rutas de los archivos de la carpeta de curricular.
            return render(request, 'archivosSolicitud.html',
                        {'cInst': cInst, 'cAcad': cAcad, 'cCurri': cCurri, 'folio': solicitud})#Regresa la plantilla "archivosSolicitud.html" para que el usuario vea los archivos subidos.
    else:
        return redirect('perfil')

def subirArchivos(request, usuario, solicitud):
    """Muestra al usuario los comentarios que ha recibido en su respectiva solicitud y
    se le solicita que vuelva a subir los archivos necesarios.

    Parámetros
    -:param request: Contiene información del navegador del usuario esta realizando la petición.
    -:param usuario: Contiene el ID del usuario que está hacinedo la consulta.
    -:param solicitud: Contiene el ID de la solicitud que ha seleccionado para volver a subir los archivos corregidos.

    Retorna
    -:return: Regresa la vista en la cual el usuario podrá ver los comentarios dados por el personal de los departamentos hacia la solicitud.
    """
    if request.user.tipo_usuario == '1'or request.user.tipo_usuario == '5':
        sol = Solicitud.objects.get(id=solicitud)#Obtenemos la solicitud seleccionada desde la base de datos.
        Coment = Comentarios.objects.filter(solicitud_id=solicitud, departamento=sol.estatus)#Obtenemos los comentarios correspontiendes a la solicitud y dadas por su departamento actual.
        comentario = ""#Inicializa variable "comentairio" en vacío.
        for element in Coment:#Ciclo que recorre todos los registros que se tienen en la variable "Coment"
            comentario = comentario + str(element.archivo)#Concatena cuales son los archivos que tienen comentarios de forma "2_12_22_3", donde cada archivo seria {2_1, 2_2, 2_3}
        if sol.nivel == '1':#Si la solicitud es de nivel media superior
            return render(request, 'subirArchivosMedSup.html',
                        {'solicitud': sol,
                        'comentarios': comentario,
                        'coment': Coment})#Muestra la plantilla "subirArchivosMedSup.html", para que la instución actualice los archivos necesarios de la carpeta Media Superior.
        else:#Si la solicitud es de nivel superior
            return render(request, 'subirArchivosSup.html',
                        {'solicitud': sol,
                        'comentarios': comentario,
                        'coment': Coment})#Muestra la plantilla "subirArchivosSup.html", para que la instución actualice los archivos necesarios de las carpetas de Superior.
    else:
        return redirect('perfil')

def terminarSubArchivos(request, usuario, solicitud):
    """Este método actualiza en la base de datos los nuevos archivos, además marca que la solicitud
    ya no tiene comentarios (por haber actualizado los archivos) y notifica al personal del departamento
    correspondiente que han actualizado los archivos de esa solicitud y se le notifica al mismo usuario
    que sus modificaciones han sido enviadas.

    Parámetros
    -:param request: Contiene información del navegador del usuario que está realizando la petición.
    -:param usuario: Contiene el ID de la institución y se utiliza para notificar a la insitución que se han enviado sus modificaciones.
    -:param solicitud: Contiene el ID de la solicitud que ha seleccionado para volver a subir los archivos corregidos.

    Retorna
    -:return redirect 'estado': Regresa la vista en la cual el usuario podrá ver la pantalla en la que aparecerá su solicitud en forma de lista.
    -:return redirect 'subirArchivos': Regresa la vista en la cual el usuario podrá ver los comentarios dados por el personal de los departamentos hacia la solicitud y pueda actualizar los documentos.

    *EXPLICACIÓN DE IDENTIFICACIÓN DE ARCHIVO DE LOS COMENTARIOS

    Los comentarios en el modelo vienen con un campo llamado "archivo" el cual es una representación del
    método de identificación individual del documento que se ideo para una fácil identificación. En este
    campo se incluyen 2 valores númericos separados por un guión bajo (#_#). El primero número representa
    la carpeta a la que corresponde dicho archivo, siendo así 1: Media superior, 2: Institucional, 3:
    Curricular, 4: Academica. El segundo número representa que documento es, por ejemplo, 1: Solicitud, 2:
    Folio de pago, 3: Personal docente, lo que representa este número depende del primer número.
    """
    if request.user.tipo_usuario == '1'or request.user.tipo_usuario == '5':
        if request.method == 'POST':#Si la solicitud es con el método POST
            request.POST._mutable = True#Permitimos la edición de lo que se recibe por el método POST
            IsLoSolicitud = Solicitud.objects.get(id=solicitud)#Solicitud que recibirá la actualización de documentos.
            Coment = Comentarios.objects.filter(solicitud_id=solicitud, departamento=IsLoSolicitud.estatus)#Obtenemos los comentarios correspondientes a la solicitud y dadas por su departamento actual.
            comentario = ""#Inicializa variable "comentario" en vacío.
            for element in Coment:#Ciclo que recorre todos los registros que se tienen en la variable "Coment"
                comentario = comentario + str(element.archivo)#Concatena cuales son los archivos que tienen comentarios de forma "2_12_22_3", donde cada archivo seria {2_1, 2_2, 2_3}
            if IsLoSolicitud.nivel == '1':#Si la solicitud es de nivel media superior
                medSup = CMedSuperior.objects.get(id_solicitud=solicitud)#Obtenemos la carpeta de media superior de la solicitud correspondiente.
                if not ("1_1" in comentario):#Si el archivo de solicitud (1_1) no tiene comentarios, manda lo existente en la carpeta media superior a su respectivo campo en la solicitud "request"
                    request.FILES["solicitud"] = medSup.solicitud
                if not ("1_2" in comentario):#Si el archivo de solicitud (1_2) no tiene comentarios, manda lo existente en la carpeta media superior a su respectivo campo en la solicitud "request"
                    request.FILES["pago"] = medSup.pago
                    request.POST["folio_pago"] = medSup.folio_pago
                    request.POST["monto_pago"] = medSup.monto_pago
                    request.POST["fecha_pago"] = medSup.fecha_pago
                if not ("1_3" in comentario):
                    request.FILES["identificacion"] = medSup.identificacion
                if not ("1_4" in comentario):
                    request.FILES["perDocente"] = medSup.perDocente
                if not ("1_5" in comentario):
                    request.FILES["instalaciones"] = medSup.instalaciones
                    request.POST["dictamen_suelo"] = medSup.dictamen_suelo
                    request.POST["expediente_suelo"] = medSup.expediente_suelo
                    request.POST["fecha_suelo"] = medSup.fecha_suelo
                    request.POST["firma_suelo"] = medSup.firma_suelo
                    request.POST["dictamen_estructural"] = medSup.dictamen_estructural
                    request.POST["fecha_estructural"] = medSup.fecha_estructural
                    request.POST["arqui_dictamen_estructural"] = medSup.arqui_dictamen_estructural
                    request.POST["noCedula_dictamen_estructural"] = medSup.noCedula_dictamen_estructural
                    request.POST["DRO_dictamen_estructural"] = medSup.DRO_dictamen_estructural
                    request.POST["dictamen_proteccion"] = medSup.dictamen_proteccion
                    request.POST["fecha_dictamen_proteccion"] = medSup.fecha_dictamen_proteccion
                    request.POST["firma_dictamen_proteccion"] = medSup.firma_dictamen_proteccion
                    request.POST["folio_inife"] = medSup.folio_inife
                    request.POST["fecha_inife"] = medSup.fecha_inife
                    request.POST["firma_inife"] = medSup.firma_inife
                if not ("1_6" in comentario):
                    request.FILES["equipamiento"] = medSup.equipamiento
                if not ("1_7" in comentario):#Si el archivo de solicitud (1_7) no tiene comentarios
                    if medSup.progEstuio == None:#Si en la carpeta de media superior no tiene un documento de planes y programas de estudio
                        progEstuio = None#Se deja igual, ya que si no tiene comentarios quiere decir que no hace falta guardar este documento.
                    else:#Si en la carpeta de media superior tiene un documento de planes y programas de estudio
                        progEstuio = medSup.progEstuio#Se guarda el archivo que se tenía antes en la carpeta de media superior
                else:#Si el archivo de solicitud (1_7) sí tiene comentarios
                    progEstuio = request.FILES["progEstuio"]#Se guarda el documento que viene desde el request
                if not ("1_8" in comentario):
                    request.FILES["cifrhs"] = medSup.cifrhs
                if not ("1_9" in comentario):
                    request.FILES["carta"] = medSup.carta
                #Se crean variables con los valores actualizados para crear un nuevo registro y borrar el anterior
                sol = request.FILES["solicitud"]
                pago = request.FILES["pago"]
                folio_pago = request.POST["folio_pago"]
                monto_pago = request.POST["monto_pago"]
                fecha_pago = request.POST["fecha_pago"]
                identificacion = request.FILES["identificacion"]
                perDocente = request.FILES["perDocente"]
                instalaciones = request.FILES["instalaciones"]
                dictamen_suelo = request.POST["dictamen_suelo"]
                expediente_suelo = request.POST["expediente_suelo"]
                fecha_suelo = request.POST["fecha_suelo"]
                firma_suelo = request.POST["firma_suelo"]
                dictamen_estructural = request.POST["dictamen_estructural"]
                fecha_estructural = request.POST["fecha_estructural"]
                arqui_dictamen_estructural = request.POST["arqui_dictamen_estructural"]
                noCedula_dictamen_estructural = request.POST["noCedula_dictamen_estructural"]
                DRO_dictamen_estructural = request.POST["DRO_dictamen_estructural"]
                dictamen_proteccion = request.POST["dictamen_proteccion"]
                fecha_dictamen_proteccion = request.POST["fecha_dictamen_proteccion"]
                firma_dictamen_proteccion = request.POST["firma_dictamen_proteccion"]
                folio_inife = request.POST["folio_inife"]
                fecha_inife = request.POST["fecha_inife"]
                firma_inife = request.POST["firma_inife"]
                equipamiento = request.FILES["equipamiento"]
                cifrhs = request.FILES["cifrhs"]
                carta = request.FILES["carta"]
                soli = Solicitud.objects.get(id=int(solicitud))#Obtenemos una instancia de la solicitud (a lo mejor se puede borrar y utilizar la creada anteriormente [IsLoSolicitud])
                medSup.delete()#Borramos el registro de la carpeta media superior que se tenía de esta solicitud
                newMedSup = CMedSuperior(id_solicitud=soli, solicitud=sol, pago=pago,
                                        folio_pago=folio_pago, monto_pago=monto_pago,
                                        fecha_pago=fecha_pago, identificacion=identificacion,
                                        perDocente=perDocente, instalaciones=instalaciones,
                                        dictamen_suelo=dictamen_suelo, expediente_suelo=expediente_suelo,
                                        fecha_suelo=fecha_suelo, firma_suelo=firma_suelo,
                                        dictamen_estructural=dictamen_estructural, fecha_estructural=fecha_estructural,
                                        arqui_dictamen_estructural=arqui_dictamen_estructural,
                                        noCedula_dictamen_estructural=noCedula_dictamen_estructural,
                                        DRO_dictamen_estructural=DRO_dictamen_estructural,
                                        dictamen_proteccion=dictamen_proteccion,
                                        fecha_dictamen_proteccion=fecha_dictamen_proteccion,
                                        firma_dictamen_proteccion=firma_dictamen_proteccion,
                                        folio_inife=folio_inife, fecha_inife=fecha_inife,
                                        firma_inife=firma_inife, equipamiento=equipamiento, progEstuio=progEstuio,
                                        cifrhs=cifrhs, carta=carta)#Creamos la plantilla de un nuevo registro con la información actualizada)#Creamos la plantilla de un nuevo registro con la información actualizada
                newMedSup.save()#Guardamos el registro de los nuevos datos de la carpeta media superior.
            else:#Si la solicitud es de nivel superior
                #Si la carpeta institucional tiene comentarios
                if ("2_1" in comentario) or ("2_2" in comentario) or ("2_3" in comentario) or (
                        "2_4" in comentario) or ("2_5" in comentario) or ("2_6" in comentario) or (
                        "2_7" in comentario) or ("2_8" in comentario) or ("2_9" in comentario) or (
                        "2_10" in comentario) or ("2_11" in comentario):
                    inst = CInstitucional.objects.get(id_solicitud=solicitud)
                    if not ("2_1" in comentario):
                        request.FILES["solicitud"] = inst.solicitud.url
                    if not ("2_2" in comentario):
                        request.FILES["pago"] = inst.pago.url
                        request.POST["folio_pago"] = inst.folio_pago
                        request.POST["monto_pago"] = inst.monto_pago
                        request.POST["fecha_pago"] = inst.fecha_pago
                    if not ("2_3" in comentario):
                        request.FILES["acredita_personalidad"] = inst.acredita_personalidad.url
                    if not ("2_4" in comentario):
                        request.FILES["acredita_inmueble"] = inst.acredita_inmueble.url
                    if not ("2_5" in comentario):
                        request.FILES["licencia_suelo"] = inst.licencia_suelo.url
                        request.POST["dictamen_suelo"] = inst.dictamen_suelo
                        request.POST["expediente_suelo"] = inst.expediente_suelo
                        request.POST["fecha_suelo"] = inst.fecha_suelo
                        request.POST["firma_suelo"] = inst.firma_suelo
                    if not ("2_6" in comentario):
                        request.FILES["constancia_estructural"] = inst.constancia_estructural.url
                        request.POST["dictamen_estructural"] = inst.dictamen_estructural
                        request.POST["fecha_estructural"] = inst.fecha_estructural
                        request.POST["arqui_dictamen_estructural"] = inst.arqui_dictamen_estructural
                        request.POST["noCedula_dictamen_estructural"] = inst.noCedula_dictamen_estructural
                        request.POST["DRO_dictamen_estructural"] = inst.DRO_dictamen_estructural
                    if not ("2_7" in comentario):
                        request.FILES["constancia_proteccion"] = inst.constancia_proteccion.url
                        request.POST["dictamen_proteccion"] = inst.dictamen_proteccion
                        request.POST["fecha_dictamen_proteccion"] = inst.fecha_dictamen_proteccion
                        request.POST["firma_dictamen_proteccion"] = inst.firma_dictamen_proteccion
                    if not ("2_8" in comentario):
                        request.FILES["inife"] = inst.inife.url
                        request.POST["folio_inife"] = inst.folio_inife
                        request.POST["fecha_inife"] = inst.fecha_inife
                        request.POST["firma_inife"] = inst.firma_inife
                    if not ("2_9" in comentario):
                        request.FILES["des_instalacion"] = inst.des_instalacion.url
                    if not ("2_10" in comentario):
                        request.FILES["planos"] = inst.planos.url
                    if not ("2_11" in comentario):
                        request.FILES["biblio"] = inst.biblio.url
                    sol = request.FILES["solicitud"]
                    pago = request.FILES["pago"]
                    folio_pago = request.POST["folio_pago"]
                    monto_pago = request.POST["monto_pago"]
                    fecha_pago = request.POST["fecha_pago"]
                    acredita_personalidad = request.FILES["acredita_personalidad"]
                    acredita_inmueble = request.FILES["acredita_inmueble"]
                    licencia_suelo = request.FILES["licencia_suelo"]
                    dictamen_suelo = request.POST["dictamen_suelo"]
                    expediente_suelo = request.POST["expediente_suelo"]
                    fecha_suelo = request.POST["fecha_suelo"]
                    firma_suelo = request.POST["firma_suelo"]
                    constancia_estructural = request.FILES["constancia_estructural"]
                    dictamen_estructural = request.POST["dictamen_estructural"]
                    fecha_estructural = request.POST["fecha_estructural"]
                    arqui_dictamen_estructural = request.POST["arqui_dictamen_estructural"]
                    noCedula_dictamen_estructural = request.POST["noCedula_dictamen_estructural"]
                    DRO_dictamen_estructural = request.POST["DRO_dictamen_estructural"]
                    constancia_proteccion = request.FILES["constancia_proteccion"]
                    dictamen_proteccion = request.POST["dictamen_proteccion"]
                    fecha_dictamen_proteccion = request.POST["fecha_dictamen_proteccion"]
                    firma_dictamen_proteccion = request.POST["firma_dictamen_proteccion"]
                    inife = request.FILES["inife"]
                    folio_inife = request.POST["folio_inife"]
                    fecha_inife = request.POST["fecha_inife"]
                    firma_inife = request.POST["firma_inife"]
                    des_instalacion = request.FILES["des_instalacion"]
                    planos = request.FILES["planos"]
                    biblio = request.FILES["biblio"]
                    soli = Solicitud.objects.get(id=int(solicitud))
                    inst.delete()
                    newInst = CInstitucional(id_solicitud=soli, solicitud=sol, pago=pago,
                                            folio_pago=folio_pago, monto_pago=monto_pago, fecha_pago=fecha_pago,
                                            acredita_personalidad=acredita_personalidad,
                                            acredita_inmueble=acredita_inmueble, licencia_suelo=licencia_suelo,
                                            dictamen_suelo=dictamen_suelo, expediente_suelo=expediente_suelo,
                                            fecha_suelo=fecha_suelo, firma_suelo=firma_suelo,
                                            constancia_estructural=constancia_estructural,
                                            dictamen_estructural=dictamen_estructural,
                                            fecha_estructural=fecha_estructural,
                                            arqui_dictamen_estructural=arqui_dictamen_estructural,
                                            noCedula_dictamen_estructural=noCedula_dictamen_estructural,
                                            DRO_dictamen_estructural=DRO_dictamen_estructural,
                                            constancia_proteccion=constancia_proteccion,
                                            dictamen_proteccion=dictamen_proteccion,
                                            fecha_dictamen_proteccion=fecha_dictamen_proteccion,
                                            firma_dictamen_proteccion=firma_dictamen_proteccion,
                                            inife=inife, folio_inife=folio_inife, fecha_inife=fecha_inife,
                                            firma_inife=firma_inife, des_instalacion=des_instalacion,
                                            planos=planos, biblio=biblio)
                    newInst.save()
                #Si la carpeta curricular tiene comentarios
                if ("3_1" in comentario) or ("3_2" in comentario) or ("3_3" in comentario) or (
                        "3_4" in comentario) or ("3_5" in comentario) or ("3_6" in comentario) or (
                        "3_7" in comentario):
                    curr = CCurricular.objects.get(id_solicitud=solicitud)
                    if not ("3_1" in comentario):
                        request.FILES["estudio"] = curr.estudio.url
                    if not ("3_2" in comentario):
                        request.FILES["plan"] = curr.plan.url
                    if not ("3_3" in comentario):
                        request.FILES["mapa"] = curr.mapa.url
                    if not ("3_4" in comentario):
                        request.FILES["programa"] = curr.programa.url
                    if not ("3_5" in comentario):
                        if curr.metodologia == None:
                            metodologia = None
                        else:
                            metodologia = curr.metodologia
                    else:
                        metodologia = request.FILES["metodologia"]
                    if not ("3_6" in comentario):
                        if curr.cifrhs == None:
                            cifrhs = None
                        else:
                            cifrhs = curr.cifrhs
                    else:
                        cifrhs = request.FILES["cifrhs"]
                    if not ("3_7" in comentario):
                        if curr.carta == None:
                            carta = None
                        else:
                            carta = curr.carta
                    else:
                        carta = request.FILES["carta"]
                    estudio = request.FILES["estudio"]
                    plan = request.FILES["plan"]
                    mapa = request.FILES["mapa"]
                    programa = request.FILES["programa"]
                    soli = Solicitud.objects.get(id=int(solicitud))
                    curr.delete()
                    newCurr = CCurricular(id_solicitud=soli, estudio=estudio, plan=plan,
                                        mapa=mapa, programa=programa, metodologia=metodologia,
                                        cifrhs=cifrhs, carta=carta)
                    newCurr.save()
                #Si la carpeta académica tiene comentarios
                if ("4_1" in comentario) or ("4_2" in comentario) or ("4_3" in comentario) or (
                        "4_4" in comentario) or ("4_5" in comentario) or ("4_6" in comentario):
                    acad = CAcademica.objects.get(id_solicitud=solicitud)
                    if not ("4_1" in comentario):
                        request.FILES["rec_bibliograficos"] = acad.rec_bibliograficos.url
                    if not ("4_2" in comentario):
                        request.FILES["rec_didacticos"] = acad.rec_didacticos.url
                    if not ("4_3" in comentario):
                        request.FILES["talleres"] = acad.talleres.url
                    if not ("4_4" in comentario):
                        request.FILES["apoyo_informatico"] = acad.apoyo_informatico.url
                    if not ("4_5" in comentario):
                        request.FILES["apoyo_comunicaciones"] = acad.apoyo_comunicaciones.url
                    if not ("4_6" in comentario):
                        request.FILES["personal"] = acad.personal.url
                    rec_bibliograficos = request.FILES["rec_bibliograficos"]
                    rec_didacticos = request.FILES["rec_didacticos"]
                    talleres = request.FILES["talleres"]
                    apoyo_informatico = request.FILES["apoyo_informatico"]
                    apoyo_comunicaciones = request.FILES["apoyo_comunicaciones"]
                    personal = request.FILES["personal"]
                    soli = Solicitud.objects.get(id=int(solicitud))
                    acad.delete()
                    newAcad = CAcademica(id_solicitud=soli, rec_bibliograficos=rec_bibliograficos,
                                        rec_didacticos=rec_didacticos, talleres=talleres,
                                        apoyo_informatico=apoyo_informatico, apoyo_comunicaciones=apoyo_comunicaciones,
                                        personal=personal)
                    newAcad.save()
            import datetime
            Solicitud.objects.filter(id=solicitud).update(comentario='2')#Actualiza el campo comentario de la solicitud a 2, para tener referencia de que la solicitud ya ha pasado por el proceso de actualización de documentos, ya que solo puede actualizar una vez los archivos por departamento.
            usuario = Solicitud.objects.values_list('customuser_id').get(id=solicitud)[0]#Obtiene el ID del usuario correspondiente a la solicitud (Creo que también se puede borrar y utilizar el que se cibe de parametro).
            notificacionU = Notificacion(solicitud_id=solicitud,
                                        descripcion="Subiste nuevamente los archivos requeridos.",
                                        leida='0',
                                        fechaNotificacion=datetime.datetime.now(),
                                        tipo_notificacion='H',
                                        usuario_id=usuario)#Crea plantilla de registro de notificación para la institución.
            notificacionU.save()#Guarda el registro de la notificación para la institución.
            Estatus = Solicitud.objects.values_list("estatus").get(id=solicitud)[0]#Se obtiene en que departamento se encuentra dicha solicitud.
            JefeSigDept = CustomUser.objects.values_list('id').get(jefe='1', departamento_id=Estatus)[0]#Extrae el id del jefe del área en que está la solicitud
            notificacionA = Notificacion(solicitud_id=solicitud,
                                        descripcion="A una solicitud le fueron subidos nuevos archivos",
                                        leida='0',
                                        fechaNotificacion=datetime.datetime.now(),
                                        tipo_notificacion='P',
                                        usuario_id=JefeSigDept)#Crea plantilla de registro de notificación para el jefe del departamento.
            notificacionA.save()#Guarda el registro de la notificación para el jefe departamento.
            return redirect('estado', usuario, solicitud)
        else:
            return redirect('subirArchivos', usuario, solicitud)
    else:
        return redirect('perfil')

def informacionPago(request, id):
    if request.user.tipo_usuario == '1' or request.user.tipo_usuario == '5':
        # Activando esta opción podremos editar los datos que vienen del método POST
        #request.POST._mutable = True
        #Obtenemos la solicitud a la cual se le va a registrar el pago
        solicitud = Solicitud.objects.get(id=id)
        from datetime import datetime
        fecha = datetime.today().strftime('%Y-%m-%d')
        error = False
        if request.method == 'POST':
            if solicitud.nivel == '1':
                form = ActPagoMedSupForm(request.POST, request.FILES)
                if form.is_valid():
                    med = CMedSuperior.objects.get(id_solicitud=id)
                    newMed = CMedSuperior(pago=request.FILES["pago"],
                                          folio_pago=request.POST["folio_pago"], monto_pago=request.POST["monto_pago"],
                                          fecha_pago=request.POST["fecha_pago"], id_solicitud=solicitud,
                                          identificacion=med.identificacion,
                                          perDocente=med.perDocente, instalaciones=med.instalaciones,
                                          dictamen_suelo=med.dictamen_suelo, expediente_suelo=med.expediente_suelo,
                                          fecha_suelo=med.fecha_suelo, firma_suelo=med.firma_suelo,
                                          dictamen_estructural=med.dictamen_estructural,
                                          fecha_estructural=med.fecha_estructural,
                                          arqui_dictamen_estructural=med.arqui_dictamen_estructural,
                                          noCedula_dictamen_estructural=med.noCedula_dictamen_estructural,
                                          DRO_dictamen_estructural=med.DRO_dictamen_estructural,
                                          dictamen_proteccion=med.dictamen_proteccion,
                                          fecha_dictamen_proteccion=med.fecha_dictamen_proteccion,
                                          firma_dictamen_proteccion=med.firma_dictamen_proteccion,
                                          folio_inife=med.folio_inife, fecha_inife=med.fecha_inife,
                                          firma_inife=med.firma_inife, equipamiento=med.equipamiento,
                                          progEstuio=med.progEstuio, cifrhs=med.cifrhs, carta=med.carta)
                    med.delete()
                    newMed.save()
                    actualizar2Fase(solicitud.id, request.user.id)
                else:
                    error = True
                    return render(request, 'informacionPago.html', {'solicitud': solicitud,
                                                                    'fecha': fecha, 'error': error})
            if solicitud.nivel == '2':
                form = ActPagoSupForm(request.POST, request.FILES)
                if form.is_valid():
                    inst = CInstitucional.objects.get(id_solicitud=id)
                    newInst = CInstitucional(id_solicitud=solicitud, pago=request.FILES["pago"],
                                             folio_pago=request.POST["folio_pago"], monto_pago=request.POST["monto_pago"],
                                             fecha_pago=request.POST["fecha_pago"],
                                             acredita_personalidad=inst.acredita_personalidad,
                                             acredita_inmueble=inst.acredita_inmueble, licencia_suelo=inst.licencia_suelo,
                                             dictamen_suelo=inst.dictamen_suelo, expediente_suelo=inst.expediente_suelo,
                                             fecha_suelo=inst.fecha_suelo, firma_suelo=inst.firma_suelo,
                                             constancia_estructural=inst.constancia_estructural,
                                             dictamen_estructural=inst.dictamen_estructural,
                                             fecha_estructural=inst.fecha_estructural,
                                             arqui_dictamen_estructural=inst.arqui_dictamen_estructural,
                                             noCedula_dictamen_estructural=inst.noCedula_dictamen_estructural,
                                             DRO_dictamen_estructural=inst.DRO_dictamen_estructural,
                                             constancia_proteccion=inst.constancia_proteccion,
                                             dictamen_proteccion=inst.dictamen_proteccion,
                                             fecha_dictamen_proteccion=inst.fecha_dictamen_proteccion,
                                             firma_dictamen_proteccion=inst.firma_dictamen_proteccion,
                                             inife=inst.inife, folio_inife=inst.folio_inife, fecha_inife=inst.fecha_inife,
                                             firma_inife=inst.firma_inife, des_instalacion=inst.des_instalacion,
                                             planos=inst.planos, biblio=inst.biblio)
                    inst.delete()
                    newInst.save()
                    actualizar2Fase(solicitud.id, request.user.id)
                else:
                    error = True
                    return render(request, 'informacionPago.html', {'solicitud': solicitud,
                                                                    'fecha': fecha, 'error': error})
            return redirect('estado',request.user.id,'G')
        return render(request, 'informacionPago.html', {'solicitud': solicitud,
                                                        'fecha': fecha, 'error': error })
    return redirect('perfil')

def actualizar2Fase(solicitud, user):
    import datetime
    # Si ya se registro el pago, pasa a la revisión de la segunda fase
    # Si anteriomente fue revisado por el ultimo departamento, le toca a control escolar recibir documentos
    Solicitud.objects.filter(id=solicitud).update(completado=10, estatus=1)
    # Obtenemos la institución a la que le pertence la solicitud.
    usuario = Solicitud.objects.values_list('customuser_id').get(id=solicitud)[0]
    # Registramos la notificación para la institución sepa que su solicitud ya fue aceptada por todos los departamentos.
    notificacionU = Notificacion(solicitud_id=solicitud,
                                 descripcion="Tu solicitud ya pasó por todas las áreas de revisión. Ahora entrega tus documentos a ventanilla única",
                                 leida='0',
                                 fechaNotificacion=datetime.datetime.now(),
                                 tipo_notificacion='H',
                                 usuario_id=usuario)
    notificacionU.save()
    # Registramos la actividad de que la solicitud ya fue aceptada por todos los departamentos.
    actividad = Actividades(usuario_id=user,
                            descripcion='La solicitud ya fue aprobada por la última área de revisión',
                            fecha=datetime.datetime.now(),
                            solicitud_id=solicitud)
    actividad.save()
    from django.db.models import Q
    # Se obtienen todos los usuarios de personal de los departamentos (jefes(2) y subordinados(3) departamento).
    usuariosAdmin = CustomUser.objects.filter(Q(tipo_usuario=2) | Q(tipo_usuario=3))
    # Se le notifica a todo el personal que la solicitud fue aceptada por todas las áreas.
    for element in usuariosAdmin:
        notificacionA = Notificacion(solicitud_id=solicitud,
                                     descripcion='La institución ya añadió información del pago',
                                     leida='0',
                                     fechaNotificacion=datetime.datetime.now(),
                                     tipo_notificacion='P',
                                     usuario_id=element.id)
        notificacionA.save()

# --------------------------------- Vistas de usuario para "Personal del departamento" ---------------------------------------------

def administrador(request):
    """Muestra al usuario la pantalla principal correspondiente al personal departamento. En esta vista,
    el personal del departamento podrá observar una vista rápida de como va el proceso de cada solicitud de
    RVOE. El usuario tendrá la opción de escoger si quiere observar las solicitudes correspondientes a su
    departamento o si quiere observar todas las solicitudes en general. Además, al cargar esta vista, se llevará
    a cabo un análisis de todas las solicitudes, que nos permitirá determinar si alguna, que ya tenga comentarios
    y a la que no se haya vuelto a subir los documentos requeridos, excedió el tiempo establecido para realizar
    esta subida. De exceder el tiempo, la solicitud será cancelada.

    Parámetros
    -:param request: Contiene información del navegador del usuario que está realizando la petición.

    Retorna
    -:return: Regresa la vista en la cual el usuario podrá ver las solicitudes posibles a revisar.
    """
    if request.user.tipo_usuario == '2' or request.user.tipo_usuario == '3':
        import datetime
        fechaActual = datetime.date.today()#Obtenemos la fecha actual.
        estadoSolicitud = Solicitud.objects.all()#Obtenemos todas las solicitudes.
        for element in estadoSolicitud:#Ciclo que recorre todas las solicitudes obtenidas en 'estadoSolicitud'
            fechaC = Comentarios.objects.values_list('fechaComentario').filter(solicitud_id=element.id,
                                                                            departamento_id=element.estatus_id,
                                                                            mostrado='1').distinct('solicitud_id')# Variable que
                                                        #nos permite determinar si la solicitud tiene comentarios realizados por el
                                                        #departamento en que se encuentra actualmente (fechaC.exists()=false: No tiene
                                                        #comentarios, fechaC.exists()=true: Si tiene comentarios).
            if (fechaC.exists() and fechaActual > diasHabiles(fechaC[0][0])):# Si sí tiene comentarios y la fecha actual es pasada la fecha límite de subida de archivos.
                Solicitud.objects.filter(id=element.id).update(completado='-1')# Actualizamos esa solicitud a "completado='-1'", lo que representa que la solicitud fue rechazada.
                usuario = Solicitud.objects.values_list('customuser_id').get(id=element.id)[0]#Obtenemos el ID del usuario que realizó esa solicitud.
                notificacionU = Notificacion(solicitud_id=element.id,
                                            descripcion="Tu solicitud fue rechazada, excedieron los días dados para volver a subir tus archivos",
                                            leida='0',
                                            fechaNotificacion=datetime.datetime.now(),
                                            tipo_notificacion='H',
                                            usuario_id=usuario)#Plantilla para enviar notificación de que la solicitud fue rechazada, al usuario que realizó la misma.
                notificacionU.save()#Guarda el registro de la notificación para el usuario 'institución' al que le pertenece la solicitud.
        from django.db.models import Q
        #Consulta de todas las solicitudes que han terminado de subir archivos (completado:0) o que hayan terminado el proceso de revisión digital (completado:10) o que ya se recibieron documentos en físico.
        Solicitudes = Solicitud.objects.filter(Q(completado='0') | Q(completado='9') | Q(completado='10') | Q(completado='11') | Q(completado='-1')).order_by('id')
        #Cantidad de notificaciones que no han sido leídas.
        TotalNotificaciones = Notificacion.objects.filter(leida='0', tipo_notificacion='P',
                                                        usuario_id=request.user.id).count()
        #Obtiene el ID del departamento al que pertenece el usuario que realizó el request
        DepartamentoUsuario = CustomUser.objects.values_list('departamento_id').get(id=request.user.id)[0]
        #Obtiene las solicitudes que tienen el departamento al cual pertenece el usuario que realizó el request.
        SolicitudDepartamento = Solicitud.objects.filter(estatus_id=DepartamentoUsuario, completado='0').order_by('id')
        #Obtiene el nombre del departamento al cual pertenece el usuario que realizó el request.
        NombreDepartamento = Departamento.objects.values_list('nombre').get(id=DepartamentoUsuario)
        #Retorna la plantilla "administrador.html" para que pueda visualizar las solicitudes.
        return render(request, 'administrador.html',
                    {"solicitudes": Solicitudes,
                    "total": TotalNotificaciones,
                    "solicitudDepartamento": SolicitudDepartamento,
                    "NombreDepartamento": NombreDepartamento[0]})
    else:
        return redirect('perfil')

def diasHabiles(x):
    """Calcula los días hábiles restantes para que la institución pueda actualizar los archivos.

    Parámetros
    -:param x: Contiene la fecha actual.

    Retorna
    -:return: Regresa la fecha límite.
    """
    import datetime
    d = datetime.timedelta(days=7)#El método "timedelta" de la librería "datetime", nos permite obtener una
                    #variable que represente un período de tiempo, con la cual se pueden realizar operaciones
                    #con variables de tipo 'datetime'
    return x + d # Obtenemos la fecha límite para subir nuevamente los documentos requeridos.

def administradorSolicitud(request, solicitud):
    """Este método muestra la solicitud que se buscó en la vista "administrador(request)".

    Parámetros
    -:param request: Contiene información del navegador del usuario que está realizando la petición.
    -:param solicitud: Contiene el ID de la solicitud que se desea visualizar.

    Retorna
    -:return: Regresa la plantilla "administrador.html" en la cuál le va a mostrar (de existir) la solicitud de su busqueda.
    """
    if request.user.tipo_usuario == '2' or request.user.tipo_usuario == '3':
        #Consulta de la solictud por ID y completado:0 (que tiene todos los archivos completos)
        Solicitudes = Solicitud.objects.filter(id=solicitud, completado='0')
        #Conteo de notificaciones que tiene el usuario que realizó el request que no han sido leídas
        TotalNotificaciones = Notificacion.objects.filter(leida='0', tipo_notificacion='P',
                                                        usuario_id=request.user.id).count()
        #Regresa la plantilla en la que el usuario puede observar la solicitud buscada.
        return render(request, 'administrador.html', {"solicitudes": Solicitudes, "total": TotalNotificaciones})
    else:
        return redirect('perfil')

def notificacionAdministrador(request):
    """Esta vista hace una consulta de todas las notificaciones no leídas del usuario tipo administrador

    Parámetros
    -:param request: Contiene información del navegador del usuario que está realizando la petición.

    Retorna
    -:return: Regresa la plantilla "notificacionAdministrador.html" que muestra las notificaciones del personal departamento.
    """
    if request.user.tipo_usuario == '2' or request.user.tipo_usuario == '3':
        import pickle
        #Obtenemos las notificaciones no leídas de tipo 'P'(Personal administrativo)
        Notificaciones = Notificacion.objects.filter(leida='0', tipo_notificacion='P', usuario_id=request.user.id).order_by('fechaNotificacion')
        #Obtenemos el nombre del departamento al cual pertenece el usuario que realizó la solicitud.
        NombreDepartamento = Departamento.objects.values_list('nombre').get(id=request.user.departamento_id)
        #Guardamos el resultado de las notificaciones en memoria.
        s = pickle.dumps(Notificaciones)
        #Actualiza las notificaciones no leídas a leídas.
        Notificacion.objects.filter(usuario_id=request.user.id, leida='0').update(leida='1')
        #Se almacena en 'NotificacionesAuxiliar' lo referenciado por 's'.
        NotificacionesAuxiliar = pickle.loads(s)
        #Muestra la plantilla "notificacionAdministrador.html" donde el usuario podrá ver las notificaciones que no había leído.
        return render(request, 'notificacionAdministrador.html',
                    {"notificaciones": NotificacionesAuxiliar, "NombreDepartamento": NombreDepartamento[0]})
    else:
        return redirect('perfil')

def historialNotificacionesAdmin(request):
    """Esta vista hace una consulta de todas las notificaciones del usuario

    Parámetros
    -:param request: Contiene información del navegador del usuario que está realizando la petición.

    Retorna
    -:return: Regresa la plantilla "notificacionAdministrador.html" que muestra la notificaciones del personal departamento.
    """
    if request.user.tipo_usuario == '2' or request.user.tipo_usuario == '3':
        #Obtenemos las notificaciones no leídas de tipo 'P', con este caracter identificamos las notificaciones orientadas al personal administrativo.
        Notificaciones = Notificacion.objects.filter(tipo_notificacion='P', usuario_id=request.user.id).order_by('fechaNotificacion')
        #Obtenemos el nombre del departamento al cual pertenece el usuario que realizó la solicitud.
        NombreDepartamento = Departamento.objects.values_list('nombre').get(id=request.user.departamento_id)
        #Conteo de notificaciones que tiene el usuario que realizó el request que no han sido leídas
        TotalNotificaciones = Notificacion.objects.filter(leida='0', tipo_notificacion='P',
                                                        usuario_id=request.user.id).count()
        #Muestra la plantilla "notificacionAdministrador.html" donde el usuario podrá ver las notificaciones que no había leído.
        return render(request, 'notificacionAdminHistorial.html',
                    {"notificaciones": Notificaciones, "NombreDepartamento": NombreDepartamento[0],
                    "total": TotalNotificaciones})
    else:
        return redirect('perfil')

def revision(request, solicitud):
    """Este método te redirige a la vista correspondiente para que el personal del departamento
    pueda revisar la solicitud.

    Parámetros
    -:param request: Contiene información del navegador del usuario que está realizando la petición.
    -:param solicitud: Contiene el ID de la solicitud que se quiere revisar.

    Retorna
    -:return redirect 'revMedSuperior': Muestra al usuario la carpeta de media superior para su revisión.
    -:return redirect 'revInstitucional': Muestra al usuario la carpeta insitucional para su revisión.
    -:return redirect 'revCurricular': Muestra al usuario la carpeta de curricular para su revisión.
    -:return render: Muestra a usuario el mensaje de error de que no puede revisar esa solicitud.
    """
    if request.user.tipo_usuario == '2' or request.user.tipo_usuario == '3':
        #Obtenemos el nivel de la solicitud (1: media superior, 2: superior)
        nivelSolicitud = Solicitud.objects.values_list('nivel').filter(id=solicitud)
        #Obtenemos el ID del departamento al que pertenece el usuario (personal del departamento)
        departamento = Departamento.objects.values_list('id').get(id=request.user.departamento_id)[0]
        # usuarioDepartamento = UserDepart.objects.values_list('id_departamento').get(id_usuario = usuario)
        # departamento = Departamento.objects.values_list('nombre').get(id=usuarioDepartamento)[0]
        if (nivelSolicitud.exists()):#Si existe la solicitud
            if nivelSolicitud[0][0] == '1':#Si la solicitud es de nivel media superior
                return redirect('revMedSuperior', solicitud)
            if nivelSolicitud[0][0] == '2':#Si la solicitud es de nivel superior
                if (departamento != 3 and departamento != 4):#Si el departamento del usuario no es superior ni media superior. (Podría borrarse el 4)
                    return redirect('revInstitucional', solicitud)
                else:#Si la solicitud se encuentra en el departamento de media superior
                    return redirect('revCurricular', solicitud)
        else:#Si la solicitud no existe.
            return render(request, 'errorRevision.html', {"folio": solicitud})
    else:
        return redirect('perfil')

def revisionCInstitucional(request, solicitud):
    """Este método muestra la vista en que el personal del despartamento puede revisar la carpeta
    institucional y hacer comentarios.

    Parámetros
    -:param request: Contiene información del navegador del usuario que está realizando la petición.
    -:param solicitud: Contiene el ID de la solicitud la cual se quiere revisar.

    Retorna
    -:return render 'revisionCInstitucional.html': Muestra a usuario la vista en la que puede revisar los documentos subidos y hacer sus respectivos comentarios.
    -:return render 'errorRevision.html': Muestra a usuario el mensaje de error de que no puede revisar esa solicitud.
    """
    if request.user.tipo_usuario == '2' or request.user.tipo_usuario == '3':
        #Cuenta las notificaciones no leídas pertenecientes al usuario que hizo la solicitud.
        totalnotificaciones = Notificacion.objects.filter(leida='0',
                                                          tipo_notificacion='P',
                                                          usuario_id=request.user.id).count()
        #Obtiene la solicitud correspondientes al departamento que pertenece el usuario y que tengan el ID de solicitud recibido.
        records = Solicitud.objects.filter(estatus=request.user.departamento_id,
                                           id=int(solicitud))
        #Obtiene el nombre del departamento al que pertenece el usuario.
        NombreDepartamento = Departamento.objects.values_list('nombre').get(id=request.user.departamento_id)
        #Obtiene el departamento en el que se encuentra la solicitud (Podría cambiarse por records.estatus)
        solicitudDepartamento = Solicitud.objects.values_list('estatus').get(id=solicitud)[0]
        #Obtiene valores que identifican los archivos, de esa solicitud específica, a los cuales le han realizado comentarios el departamento en el que actualmente se encuentra.
        ComentarioArchivo = Comentarios.objects.values_list("archivo").filter(solicitud_id=solicitud,
                                                                            departamento=solicitudDepartamento)
        #Obtiene los comentarios que no han sido mostrados a la institución
        ComentarioArchivoNoMostrado = Comentarios.objects.filter(solicitud_id=solicitud, departamento=solicitudDepartamento,
                                                                mostrado='0')
        #Obtiene los comentarios que ya han sido mostrados a la institución.
        ComentarioArchivoMostrado = Comentarios.objects.filter(solicitud_id=solicitud, departamento=solicitudDepartamento,
                                                            mostrado='1')
        #Obtiene si la solicitud ya se le realizaron comentarios (0:No ha recibido comentarios, 1:Tiene comentarios, 2:Actualizó archivos)
        estadoComentario = Solicitud.objects.values_list("comentario").get(id=solicitud)[0]
        #Se obtiene la solicitud por ID
        datosSolicitud = Solicitud.objects.get(id=solicitud)
        #Esta variable analiza el campo 'completado' de una solicitud, para determinar si el proceso inicial de revisión ya fue completado y esta solicitud ya pasó por todas las áreas.
        noHaPasadoPorTodasLasAreas = Solicitud.objects.values_list("completado").get(id=solicitud)[0] != 10
        Coment = ""
        for element in ComentarioArchivo:#Este ciclo nos permite almacenar en la variable 'Coment', todos los valores que identifican los archivos con comentarios, almacenados en 'ComentarioArchivo'.
            Coment = Coment + str(element[0])
        #Nos permite analizar si existe una solicitud con el id proporcionado.
        for x in records:
            if solicitud == str(x.id):
                archivos = CInstitucional.objects.filter(id_solicitud=solicitud)
                return render(request, 'revisionCInstitucional.html', {
                    'archivos': archivos,
                    'folio': solicitud,
                    "total": totalnotificaciones,
                    "NombreDepartamento": NombreDepartamento[0],
                    "comentarios": Coment,
                    "estadoComentario": estadoComentario,
                    "solicitud": datosSolicitud,
                    "comentarioMostrado": ComentarioArchivoMostrado,
                    "comentarioNoMostrado": ComentarioArchivoNoMostrado,
                    "noHaPasadoPorTodasLasAreas": noHaPasadoPorTodasLasAreas
                })
        return render(request, 'errorRevision.html', {"folio": solicitud})
    else:
        return redirect('perfil')

def revisionCCurricular(request, solicitud):
    """Este método muestra la vista en que el personal del despartamento puede revisar la carpeta
    curricular y hacer comentarios.

    Parámetros
    -:param request: Contiene información del navegador del usuario que está realizando la petición.
    -:param solicitud: Contiene el ID de la solicitud que se quiere revisar.

    Retorna
    -:return render 'revisionCCurricular.html': Muestra a usuario la vista en la que puede revisar los documentos subidos y hacer sus respectivos comentarios.
    -:return render 'errorRevision.html': Muestra a usuario el mensaje de error de que no puede revisar esa solicitud.
    """
    if request.user.tipo_usuario == '2' or request.user.tipo_usuario == '3':
        #Cuenta las notificaciones no leídas pertenecientes al usuario que hizo la solicitud.
        totalnotificaciones = Notificacion.objects.filter(leida='0', tipo_notificacion='P',
                                                        usuario_id=request.user.id).count()
        #Obtiene la solicitud correspondientes al departamento que pertenece el usuario y que tengan el ID de solicitud recibido.
        records = Solicitud.objects.filter(estatus=request.user.departamento_id, id=int(solicitud))
        #Obtiene el nombre del departamento al que pertenece el usuario.
        NombreDepartamento = Departamento.objects.values_list('nombre').get(id=request.user.departamento_id)
        #Obtiene el departamento en el que se encuentra la solicitud (Podría cambiarse por records.estatus)
        solicitudDepartamento = Solicitud.objects.values_list('estatus').get(id=solicitud)[0]
        #Obtiene los comentarios recibidos de la solicitud que fueron hechos por el departamento del usuario correspondiente.
        ComentarioArchivo = Comentarios.objects.values_list("archivo").filter(solicitud_id=solicitud,
                                                                            departamento=solicitudDepartamento)
        #Se obtiene la solicitud por ID
        datosSolicitud = Solicitud.objects.get(id=solicitud)
        #
        noHaPasadoPorTodasLasAreas = Solicitud.objects.values_list("completado").get(id=solicitud)[0] != 10
        Coment = ""
        for element in ComentarioArchivo:
            Coment = Coment + str(element[0])
        #
        for x in records:
            if solicitud == str(x.id):
                archivos = CCurricular.objects.filter(id_solicitud=solicitud)
                return render(request, 'revisionCCurricular.html', {
                    'archivos': archivos,
                    'folio': solicitud,
                    "total": totalnotificaciones,
                    "NombreDepartamento": NombreDepartamento[0],
                    "comentarios": Coment,
                    "solicitud": datosSolicitud,
                    "noHaPasadoPorTodasLasAreas": noHaPasadoPorTodasLasAreas
                })
        return render(request, 'errorRevision.html', {"folio": solicitud})
    else:
        return redirect('perfil')

def revisionCAcademica(request, solicitud):
    """Este método muestra la vista en que el personal del despartamento puede revisar la carpeta
    académica y hacer comentarios.

    Parámetros
    -:param request: Contiene información del navegador del usuario que está realizando la petición.
    -:param solicitud: Contiene el ID de la solicitud que se quiere revisar.

    Retorna
    -:return render 'revisionCAcademica.html': Muestra a usuario la vista en la que puede revisar los documentos subidos y hacer sus respectivos comentarios.
    -:return render 'errorRevision.html': Muestra a usuario el mensaje de error de que no puede revisar esa solicitud.
    """
    if request.user.tipo_usuario == '2' or request.user.tipo_usuario == '3':
        #Cuenta las notificaciones no leídas pertenecientes al usuario que hizo la solicitud.
        totalnotificaciones = Notificacion.objects.filter(leida='0', tipo_notificacion='P',
                                                        usuario_id=request.user.id).count()
        #Obtiene la solicitud correspondientes al departamento que pertenece el usuario y que tengan el ID de solicitud recibido.
        records = Solicitud.objects.filter(estatus=request.user.departamento_id, id=int(solicitud))
        #Obtiene el nombre del departamento al que pertenece el usuario.
        NombreDepartamento = Departamento.objects.values_list('nombre').get(id=request.user.departamento_id)
        #Obtiene el departamento en el que se encuentra la solicitud (Podría cambiarse por records.estatus)
        solicitudDepartamento = Solicitud.objects.values_list('estatus').get(id=solicitud)[0]
        #Obtiene los comentarios recibidos de la solicitud que fueron hechos por el departamento del usuario correspondiente.
        ComentarioArchivo = Comentarios.objects.values_list("archivo").filter(solicitud_id=solicitud,
                                                                            departamento=solicitudDepartamento)
        #Obtiene los comentarios que no han sido mostrados a la institución
        ComentarioArchivoNoMostrado = Comentarios.objects.filter(solicitud_id=solicitud, departamento=solicitudDepartamento,
                                                                mostrado='0')
        #Obtiene los comentarios que ya han sido mostrados a la institución.
        ComentarioArchivoMostrado = Comentarios.objects.filter(solicitud_id=solicitud, departamento=solicitudDepartamento,
                                                            mostrado='1')
        #Obtiene si la solicitud ya se le realizaron comentarios (0:No ha recibido comentarios, 1:Tiene comentarios, 2:Actualizó archivos)
        estadoComentario = Solicitud.objects.values_list("comentario").get(id=solicitud)[0]
        #Se obtiene la solicitud por ID
        datosSolicitud = Solicitud.objects.get(id=solicitud)
        #
        noHaPasadoPorTodasLasAreas = Solicitud.objects.values_list("completado").get(id=solicitud)[0] != 10
        Coment = ""
        for element in ComentarioArchivo:
            Coment = Coment + str(element[0])
        #
        for x in records:
            if solicitud == str(x.id):
                archivos = CAcademica.objects.filter(id_solicitud=solicitud)
                return render(request, 'revisionCAcademica.html', {
                    'archivos': archivos,
                    'folio': solicitud,
                    "total": totalnotificaciones,
                    "NombreDepartamento": NombreDepartamento[0],
                    "comentarios": Coment,
                    "estadoComentario": estadoComentario,
                    "solicitud": datosSolicitud,
                    "comentarioMostrado": ComentarioArchivoMostrado,
                    "comentarioNoMostrado": ComentarioArchivoNoMostrado,
                    "noHaPasadoPorTodasLasAreas": noHaPasadoPorTodasLasAreas
                })
        return render(request, 'errorRevision.html', {"folio": solicitud})
    else:
        return redirect('perfil')

def revisionCMedSuperior(request, solicitud):
    """Este método muestra la vista en que el personal del despartamento puede revisar la carpeta
    de media superior y hacer comentarios.

    Parámetros
    -:param request: Contiene información del navegador del usuario que está realizando la petición.
    -:param solicitud: Contiene el ID de la solicitud que se quiere revisar.

    Retorna
    -:return render 'revisionCMedSuperior.html': Muestra a usuario la vista en la que puede revisar los documentos subidos y hacer sus respectivos comentarios.
    -:return render 'errorRevision.html': Muestra a usuario el mensaje de error de que no puede revisar esa solicitud.
    """
    if request.user.tipo_usuario == '2' or request.user.tipo_usuario == '3':
        #Cuenta las notificaciones no leídas pertenecientes al usuario que hizo la solicitud.
        totalnotificaciones = Notificacion.objects.filter(leida='0',
                                                          tipo_notificacion='P',
                                                          usuario_id=request.user.id).count()
        #Obtiene el nombre del departamento al que pertenece el usuario.
        NombreDepartamento = Departamento.objects.values_list('nombre').get(id=request.user.departamento_id)
        #Obtiene la solicitudes correspondientes al departamento que pertenece el usuario y que tengan el ID de solicitud recibido.
        records = Solicitud.objects.filter(estatus=request.user.departamento_id,
                                           id=int(solicitud)).exclude(completado=11)
        #Obtiene el departamento en el que se encuentra la solicitud (Podría cambiarse por records.estatus)
        solicitudDepartamento = Solicitud.objects.values_list('estatus').get(id=solicitud)[0]
        #Obtiene los comentarios recibidos de la solicitud que fueron hechos por el departamento del usuario correspondiente.
        ComentarioArchivo = Comentarios.objects.values_list("archivo").filter(solicitud_id=solicitud,
                                                                              departamento=solicitudDepartamento)
        #Obtiene los comentarios que no han sido mostrados a la institución
        ComentarioArchivoNoMostrado = Comentarios.objects.filter(solicitud_id=solicitud,
                                                                 departamento=solicitudDepartamento,
                                                                 mostrado='0')
        #Obtiene los comentarios que ya han sido mostrados a la institución.
        ComentarioArchivoMostrado = Comentarios.objects.filter(solicitud_id=solicitud,
                                                               departamento=solicitudDepartamento,
                                                               mostrado='1')
        #Obtiene si la solicitud ya se le realizaron comentarios (0:No ha recibido comentarios, 1:Tiene comentarios, 2:Actualizó archivos)
        estadoComentario = Solicitud.objects.values_list("comentario").get(id=solicitud)[0]
        #Se obtiene la solicitud por ID
        datosSolicitud = Solicitud.objects.get(id=solicitud)
        #
        noHaPasadoPorTodasLasAreas = Solicitud.objects.values_list("completado").get(id=solicitud)[0] != 10
        Coment = ""
        for element in ComentarioArchivo:
            Coment = Coment + str(element[0])
        #
        for x in records:
            if solicitud == str(x.id):
                archivos = CMedSuperior.objects.filter(id_solicitud=solicitud)
                return render(request, 'revisionCMedSuperior.html', {
                    'archivos': archivos,
                    'folio': solicitud,
                    'nombre': x.nombreSolicitud,
                    "total": totalnotificaciones,
                    "NombreDepartamento": NombreDepartamento[0],
                    "comentarios": Coment,
                    "estadoComentario": estadoComentario,
                    "solicitud": datosSolicitud,
                    "comentarioMostrado": ComentarioArchivoMostrado,
                    "comentarioNoMostrado": ComentarioArchivoNoMostrado,
                    "noHaPasadoPorTodasLasAreas": noHaPasadoPorTodasLasAreas
                })
        return render(request, 'errorRevision.html', {"folio": solicitud})
    else:
        return redirect('perfil')

def comentariosSolicitud(request, solicitud, idArchivo, carpeta):
    """Este método se utiliza para añadir los comentarios a cada archivo de su correspondiente carpeta.

    Parámetros
    -:param request: Contiene información del navegador del usuario que está realizando la petición.
    -:param solicitud: Contiene el ID de la solicitud que se quiere revisar.
    -:param idArchivo: Contiene el identificador del archivo (#_#: carpeta_archivo) sobre el cuál se va a realizar el comentario.
    -:param carpeta: Nos indica la carpeta en la que se encuentra el usuario haciendo la revisión.

    Retorna
    -:return redirect: Redirige a la vista en la que el usuario estaba haciendo la revisión.
    """
    if request.user.tipo_usuario == '2' or request.user.tipo_usuario == '3':
        if request.method == 'POST' and idArchivo != 'mostrar':
            import datetime
            #Obtenemos el id del departamento de la persona que está haciendo la revisión.
            IDDepartamento = CustomUser.objects.values_list('departamento_id').get(id=request.user.id)
            #Guardamos en una variable el valor que se tenga en el campo descripción en la plantilla.
            comentario = request.POST["descripcion"]
            #Se obtiene la fecha actal.
            fechaCom = datetime.datetime.now()
            #Se inserta el comentario en la base de datos para que los usuarios posteriormente las revisen.
            comentario = Comentarios(solicitud_id=solicitud, descripcion=comentario,
                                    fechaComentario=fechaCom, mostrado='0', archivo=idArchivo,
                                    departamento_id=IDDepartamento[0])
            comentario.save()
            return redirect('/inicio/admin/archivos/' + solicitud + '/' + carpeta + '/')
    else:
        return redirect('perfil')

def comentariosTerminado(request, solicitud):
    """Este método se utiliza para:
    1. Rechazar la solicitud en caso de que esta ya haya recibido comentarios anteriormente por el mismo departamento.
    2. De tener comentarios le muestra los comentarios a la institución.
    3. De no tener comentarios pasa la solicitud a la siguiente área.
    Además en cada opción se registra la actividad realizada por el usuario.

    Parámetros
    -:param request: Contiene información del navegador del usuario que está realizando la petición.
    -:param solicitud: Contiene el ID de la solicitud que se quiere revisar.

    Retorna
    :return redirect: Redirige a la pantalla principal del personal del departamento.
    """
    if request.user.tipo_usuario == '2' or request.user.tipo_usuario == '3':
        import datetime
        #Obtiene un valor booleano para identificar si no le han mostrado los comentarios a la institución.
        tieneComentariosPorMostrar = Comentarios.objects.filter(solicitud_id=solicitud, mostrado=0).exists()

        #   1. Rechazar la solicitud en caso de que esta ya haya recibido comentarios anteriormente por el mismo departamento.
        #Si ya actualizó archivos y vuelve a tener comentarios en la solicitud sin mostrar.
        if (Solicitud.objects.values_list('comentario').get(id=solicitud)[0] == '2' and tieneComentariosPorMostrar):
            #Actualiza la solicitud a "completado=-1", para identificar que la solicitud a sido rechazada.
            Solicitud.objects.filter(id=solicitud).update(completado=(-1))
            #Obtenemos el usuario (institución) correspondiente a esa solicitud.
            usuario = Solicitud.objects.values_list('customuser_id').get(id=solicitud)[0]
            #Registro para notificar al usuario que su solicitud ha sido rechazada.
            notificacionU = Notificacion(solicitud_id=solicitud,
                                        descripcion="Tu solicitud fue rechazada",
                                        leida='0',
                                        fechaNotificacion=datetime.datetime.now(),
                                        tipo_notificacion='H',
                                        usuario_id=usuario)
            notificacionU.save()
            #Registro para tener el control de que la solicitud fue rechazada por incumplimiento de requisitos.
            actividad = Actividades(usuario_id=request.user.id,
                                    descripcion='La solicitud fue rechazada por incumplimiento de requisitos.',
                                    fecha=datetime.datetime.now(),
                                    solicitud_id=solicitud)
            actividad.save()
            return redirect('admin')

        #   2. De tener comentarios le muestra los comentarios a la institución.
        if tieneComentariosPorMostrar:
            #Obtenemos si la solicitud tiene comentarios (comentario=0: no tiene comentarios, comentario=1: tiene comentarios)
            solicitudes = Solicitud.objects.values_list('comentario').get(id=solicitud)[0]
            #Si la solicitud no tiene comentarios.
            if (solicitudes == '0'):
                #Actualizamos la solicitud para decir que ha recibido comentarios.
                Solicitud.objects.filter(id=solicitud).update(comentario='1')
            #Actualizamos los comentarios de la solicitud que no han sido mostrados(=0) a mostrados(=1)
            Comentarios.objects.filter(solicitud_id=solicitud, mostrado=0).update(mostrado='1',
                                                                                fechaComentario=datetime.datetime.now())
            #Obtenemos la institución a la que le pertenece la solicitud.
            usuario = Solicitud.objects.values_list('customuser_id').get(id=solicitud)[0]
            #Registramos la notificación de que la solicitud ha recibido comentarios.
            notificacionU = Notificacion(solicitud_id=solicitud,
                                        descripcion="Se realizaron observaciones a esta solicitud",
                                        leida='0',
                                        fechaNotificacion=datetime.datetime.now(),
                                        tipo_notificacion='H',
                                        usuario_id=usuario)
            notificacionU.save()
            #Registramos la actividad de que se le realizaron comentarios a esta solicitud.
            actividad = Actividades(usuario_id=request.user.id,
                                    descripcion='Realizó observaciones a la solicitud.',
                                    fecha=datetime.datetime.now(),
                                    solicitud_id=solicitud)
            actividad.save()
        #   3. De no tener comentarios pasa la solicitud a la siguiente área.
        else:
            #Obtenemos el nivel de la solicitud(1:media superior, 2:superior)
            nivelSolicitud = Solicitud.objects.values_list('nivel').get(id=solicitud)[0]
            #Obtenemos el departamento en el que se encuentra la solicitud.
            estatusSolicitud = Solicitud.objects.values_list('estatus').get(id=solicitud)[0]
            #Inicializamos la variable para establecer el siguiente departamento que revisará la solicitud.
            siguienteDepartamento = 0
            #Si la solicitud se encuentra en el departamento Dirección y es de media superior
            if (estatusSolicitud == 2 and nivelSolicitud == '1'):
                #Establecemos que el siguiente departamento a revisar será Media superior
                siguienteDepartamento = 4
            else:
                #validamos si se encuentra en el departamento de superior y es una solicitud de superior
                if (estatusSolicitud == 3 and nivelSolicitud == '2'):
                    #Establecemos 5 en siguiente departamento para que pueda regresar a control escolar y pida documentos en fisico
                    siguienteDepartamento = 5
                else:
                    #La solicitud pasa al siguiente departamento en lista (Control escolar->Dirección->Superior)
                    siguienteDepartamento = estatusSolicitud + 1
            #Obtenemos la institución a la que le pertence la solicitud.
            usuario = Solicitud.objects.values_list('customuser_id').get(id=solicitud)[0]
            #Obtenemos en que estado se encuentra la solicitud (Completo, rechazado o finalizado)
            completado = Solicitud.objects.values_list('completado').get(id=solicitud)[0]
            #Si el siguiente departamento no es el 5 (no existe un quinto departamento) y no ha pasado anteriormente por todos los departamentos
            if ((siguienteDepartamento != 5) and (completado != 10)):
                #Obtenemos el nombre del siguiente departamento
                NombreDepartamento = Departamento.objects.values_list('nombre').get(id=(siguienteDepartamento))[0]
                #Acualizamos la solicitud para definir quien es el siguiente departamento a revisar la solicitud y actualizamos que no se ha recibido comentarios.
                Solicitud.objects.filter(id=solicitud).update(estatus=siguienteDepartamento, comentario=0)
                #Notificamos a la institución que su solicitud pasó a la siguiente área.
                notificacionU = Notificacion(solicitud_id=solicitud,
                                            descripcion="Tu solicitud pasó a una siguiente área: " + NombreDepartamento,
                                            leida='0',
                                            fechaNotificacion=datetime.datetime.now(),
                                            tipo_notificacion='H',
                                            usuario_id=usuario)
                notificacionU.save()
                # Extrae el id del jefe de la siguiente área que le toca realizar la revisión
                usuariosAdminDept = CustomUser.objects.filter(departamento_id=(siguienteDepartamento))
                #Notificamos a todos los usuarios pertenecientes al siguiente departamento que tienen una nueva solicitud por revisar.
                for element in usuariosAdminDept:
                    notificacionA = Notificacion(solicitud_id=solicitud,
                                                descripcion="Una solicitud pasó a ser revisada por tú área",
                                                leida='0',
                                                fechaNotificacion=datetime.datetime.now(),
                                                tipo_notificacion='P',
                                                usuario_id=element.id)
                    notificacionA.save()
                #Registramos la actividad de que la solicitud pasó a ser revisada por el siguiente departamento.
                actividad = Actividades(usuario_id=request.user.id,
                                        descripcion='La solicitud pasó al departamento ' + NombreDepartamento,
                                        fecha=datetime.datetime.now(),
                                        solicitud_id=solicitud)
                actividad.save()
                '''
                #Si el departamento que hizo pasar la solicitud al siguiente departamento es "dirección"
                if ((siguienteDepartamento - 1) == 2):
                    #Se le notifica a la institución que ya puede cargar su documento de admisión de trámite.
                    notAdmision = Notificacion(solicitud_id=solicitud,
                                            descripcion="Se le ha generado su documento de admisión de tramite."
                                                        "Puede obtenerlo en la página de estado de solicitudes.",
                                            leida='0',
                                            fechaNotificacion=datetime.datetime.now(),
                                            tipo_notificacion='H',
                                            usuario_id=usuario)
                    notAdmision.save()
                '''
            #Si el siguiente departamento es 5 (no existe un departamento 5)
            else:
                #Si ya pasó por la primera fase (revisado digitalmente por dirección y el nivel)
                if completado == 0:
                    #Establecemos la solicitud para petición de pago
                    Solicitud.objects.filter(id=solicitud).update(completado=9, comentario=0)
                    # Obtenemos la institución a la que le pertence la solicitud.
                    usuario = Solicitud.objects.values_list('customuser_id').get(id=solicitud)[0]
                    # Registramos la notificación para la institución sepa que su solicitud ya fue aceptada por todos los departamentos y ahora introduzca información del pago.
                    notificacionU = Notificacion(solicitud_id=solicitud,
                                                 descripcion="Tu solicitud ha sido aceptada en la revisión digital. "
                                                             "Favor de introducir información del pago",
                                                 leida='0',
                                                 fechaNotificacion=datetime.datetime.now(),
                                                 tipo_notificacion='H',
                                                 usuario_id=usuario)
                    notificacionU.save()
                    # Registramos la actividad de que se le pidió el pagó a la institución.
                    actividad = Actividades(usuario_id=request.user.id,
                                            descripcion='Se ha pedido el pago para continuar con el proceso de la solicitud',
                                            fecha=datetime.datetime.now(),
                                            solicitud_id=solicitud)
                    actividad.save()
                    from django.db.models import Q
                    #Se obtienen todos los usuarios de personal de los departamentos (jefes(2) y subordinados(3) departamento).
                    usuariosAdmin = CustomUser.objects.filter(Q(tipo_usuario=2) | Q(tipo_usuario=3))
                    # Se le notifica a todos los jefes que la solicitud fue aceptada por todas las áreas.
                    for element in usuariosAdmin:
                        notificacionA = Notificacion(solicitud_id=solicitud,
                                                     descripcion='La solicitud ya fue aprobada por la última área de revisión y se solicitó el pagó',
                                                     leida='0',
                                                     fechaNotificacion=datetime.datetime.now(),
                                                     tipo_notificacion='P',
                                                     usuario_id=element.id)
                        notificacionA.save()
        return redirect('admin')
    else:
        return redirect('perfil')

def comentariosMostrar(request, solicitud, carpeta):
    """Muestra las comentarios que han sido ingresados por el personal a la solicitud.

    Parámetros
    -:param request: Contiene información del navegador del usuario que está realizando la petición.
    -:param solicitud: Contiene el ID de la solicitud la cual se quiere revisar.
    -:param carpeta: Nos indica la carpeta en la que se encuentra el usuario haciendo la revisión.

    Retorna
    :return render: Muestra la pantalla en la que visualiza los comentarios pertenecientes a la solicitud que se esta revisando.
    """
    if request.user.tipo_usuario == '2' or request.user.tipo_usuario == '3':
        #Obtiene el total de las notificaciones que no han sido leídas.
        TotalNotificaciones = Notificacion.objects.filter(leida='0', tipo_notificacion='P',
                                                        usuario_id=request.user.id).count()
        #Obtiene el nombre del departamento al que pertenece el usuario que realizó el request.
        NombreDepartamento = Departamento.objects.values_list('nombre').get(id=request.user.departamento_id)
        #Obtiene todos los comentarios de la solicitud.
        comentariosSolicitud = Comentarios.objects.filter(solicitud_id=solicitud)
        return render(request, 'mostrarComentarios.html',
                    {"comentarios": comentariosSolicitud,
                    "total": TotalNotificaciones,
                    "NombreDepartamento": NombreDepartamento[0],
                    "carpeta": carpeta})
    else:
        return redirect('perfil')

def comentariosEliminar(request, solicitud, idArchivo, carpeta):
    """Borra un comentario específico de la solicitud.

    Parámetros
    -:param request: Contiene información del navegador del usuario que está realizando la petición.
    -:param solicitud: Contiene el ID de la solicitud la cual se quiere revisar.
    -:param idArchivo: Contiene el id del Comentario que se desea borrar
    -:param carpeta: Nos indica la carpeta en la que se encuentra el usuario haciendo la revisión.

    Retorna
    :return redirect: Regresa a la pantalla en la que estaba haciendo la revisión.
    """
    if request.user.tipo_usuario == '2' or request.user.tipo_usuario == '3':
        Comentarios.objects.filter(id=idArchivo).delete()
        return redirect('/inicio/admin/archivos/' + solicitud + '/' + carpeta + '/')
    else:
        return redirect('perfil')

def historialActividades(request):
    """Muestra todas las acciones que ha tenido el personal del departamento sobre las solicitudes.

    Parámetros
    -:param request: Contiene información del navegador del usuario que está realizando la petición.

    Retorna
    :return render: Regresa la plantilla en la que se muestran todas las actividades que han sido realizadas por el departamento.
    """
    if request.user.tipo_usuario == '2' or request.user.tipo_usuario == '3':
        #Obtienen todas las actividades realizadas por el personal del departamento
        records = Actividades.objects.all()
        #Obtiene el total de notificaciones que no han sido leídas por el usuario.
        TotalNotificaciones = Notificacion.objects.filter(leida='0', tipo_notificacion='P',
                                                        usuario_id=request.user.id).count()
        #Obtiene el nombre del departamento al que pertenece el usuario.
        NombreDepartamento = Departamento.objects.values_list('nombre').get(id=request.user.departamento_id)
        return render(request, 'historialActividades.html',
                    {'records': records, "NombreDepartamento": NombreDepartamento[0], "total": TotalNotificaciones})
    else:
        return redirect('perfil')

def entregoDocumentosFisicos(request, solicitud):
    """Define que la institución ya entregó los documentos en físico al departamento de control escolar.

    Parámetros
    -:param request: Contiene información del navegador del usuario que está realizando la petición.
    -:param solicitud: Contiene el ID de la solicitud la cual se quiere revisar.

    Retorna
    :return redirect: Redirige a la pantalla principal del personal del departamento.
    """
    if request.user.tipo_usuario == '2' or request.user.tipo_usuario == '3':
        import datetime
        #Obtenemos el nivel de la solicitud(1:media superior, 2:superior)
        nivelSolicitud = Solicitud.objects.values_list('nivel').get(id=solicitud)[0]
        #Obtenemos el departamento en el que se encuentra la solicitud.
        estatusSolicitud = Solicitud.objects.values_list('estatus').get(id=solicitud)[0]
        NombreDepartamento = Departamento.objects.values_list('nombre').get(id=estatusSolicitud)[0]
        #Inicializamos la variable para establecer el siguiente departamento que revisará la solicitud.
        siguienteDepartamento = 0
        #Si la solicitud se encuentra en el departamento Dirección y es de media superior
        if (estatusSolicitud == 2 and nivelSolicitud == '1'):
            #Establecemos que el siguiente departamento a revisar será Media superior
            siguienteDepartamento = 4
        else:
            #La solicitud pasa al siguiente departamento en lista (Control escolar->Dirección->Superior)
            siguienteDepartamento = estatusSolicitud + 1
        #Actualizamos que la solicitud ahora le corresponde la revisión al departamento de dirección.
        Solicitud.objects.filter(id=solicitud).update(estatus=siguienteDepartamento)
        #Obtiene el ID de la institución a la que le pertenece la solicitud.
        usuario = Solicitud.objects.values_list('customuser_id').get(id=solicitud)[0]
        #Registra la notificación para la institución de que ya ha entregado los documentos en físico.
        notificacionU = Notificacion(solicitud_id=solicitud,
                                    descripcion="La documentación a pasado al departamento " + NombreDepartamento,
                                    leida='0',
                                    fechaNotificacion=datetime.datetime.now(),
                                    tipo_notificacion='H',
                                    usuario_id=usuario)
        notificacionU.save()
        from django.db.models import Q
        if (siguienteDepartamento==3 or siguienteDepartamento==4):
            #Se obtienen todos los usuarios que no pertenecen a dirección
            usuariosAdmin = CustomUser.objects.exclude(Q(departamento=siguienteDepartamento) | Q(departamento=None))
            #Se les notifica a todos los usuarios obtenidos anteriormente que tienen una solicitud pendiente por hacer la revisión de visita.
            for element in usuariosAdmin:
                notificacionA = Notificacion(solicitud_id=solicitud,
                                            descripcion='Esta solicitud esta pendiente de visita de revisión',
                                            leida='0',
                                            fechaNotificacion=datetime.datetime.now(),
                                            tipo_notificacion='P',
                                            usuario_id=element.id)
                notificacionA.save()
        #Se obtiene los usuarios que correspondan al departamento de Dirección
        usuariosDeDireccion = CustomUser.objects.filter(departamento=siguienteDepartamento)
        #Registra la notificación a todo el personal de dirección
        for element in usuariosDeDireccion:
            notificacionA = Notificacion(solicitud_id=solicitud,
                                        descripcion='La solicitud pasó nuevamente a tu área',
                                        leida='0',
                                        fechaNotificacion=datetime.datetime.now(),
                                        tipo_notificacion='P',
                                        usuario_id=element.id)
            notificacionA.save()
        return redirect('admin')
    else:
        return redirect('perfil')

def finProceso(request, solicitud):
    """Define que el proceso digital a terminado.

    Parámetros
    -:param request: Contiene información del navegador del usuario que está realizando la petición.
    -:param solicitud: Contiene el ID de la solicitud la cual se quiere revisar.

    Retorna
    :return redirect: Redirige a la pantalla principal del personal del departamento.
    """
    if request.user.tipo_usuario == '2' or request.user.tipo_usuario == '3':
        import datetime
        #Obtenemos la observación realizada por la visita
        observacion = request.POST["observacionesVisita"]
        if observacion == "":
            #Actualiza el estado de la solicitud para decir que ya ha terminado el proceso digital (completado:11)
            Solicitud.objects.filter(id=solicitud).update(completado=11)
            #Registra la actividad de que el proceso digital de la solicitud ya ha terminado.
            actividad = Actividades(usuario_id=request.user.id,
                                    descripcion='La solicitud ' + solicitud + 'ha completado el proceso digital',
                                    fecha=datetime.datetime.now(),
                                    solicitud_id=solicitud)
            actividad.save()
            #Obtiene el usuario de institución correspondiente a la solicitud.
            usuario = Solicitud.objects.values_list('customuser_id').get(id=solicitud)[0]
            #Registra la notificación para la institución, de que que su solicitud ha terminado el proceso digital.
            notificacionA = Notificacion(solicitud_id=solicitud,
                                        descripcion="La solicitud " + solicitud + " ha completado su proceso de revisión digital. "
                                                                                "Ahora comience el proceso en físico",
                                        leida='0',
                                        fechaNotificacion=datetime.datetime.now(),
                                        tipo_notificacion='H',
                                        usuario_id=usuario)
            notificacionA.save()
            #Se obtienen los usuarios de todo el personal de todos los departamentos.
            usuariosDep = CustomUser.objects.exclude(departamento_id=None)
            #Registra la notificación de que la solicitud ha completado el proceso digital.
            for element in usuariosDep:
                notificacionB = Notificacion(solicitud_id=solicitud,
                                            descripcion="La solicitud " + solicitud + " ha completado su proceso de revisión digital",
                                            leida='0',
                                            fechaNotificacion=datetime.datetime.now(),
                                            tipo_notificacion='P',
                                            usuario_id=element.id)
                notificacionB.save()
            return redirect('admin')
        else:
            #Actualiza el estado de la solicitud para decir que fue cancelada por incumplimiento de la solicitud
            Solicitud.objects.filter(id=solicitud).update(completado=-1)
            #Registra la actividad de que el proceso digital de la solicitud ya ha terminado.
            actividad = Actividades(usuario_id=request.user.id,
                                    descripcion='La solicitud ' + solicitud + ' ha sido rechazada por incumplimiento en la visita de la institución',
                                    fecha=datetime.datetime.now(),
                                    solicitud_id=solicitud)
            actividad.save()
            #Obtiene el usuario de institución correspondiente a la solicitud.
            usuario = Solicitud.objects.values_list('customuser_id').get(id=solicitud)[0]
            #Registra la notificación para la institución, de que que su solicitud ha terminado el proceso digital.
            notificacionA = Notificacion(solicitud_id=solicitud,
                                        descripcion="La solicitud " + solicitud + " ha sido rechazada por incumplimiento en la visita de la institución. "
                                                                                "("+observacion+")",
                                        leida='0',
                                        fechaNotificacion=datetime.datetime.now(),
                                        tipo_notificacion='H',
                                        usuario_id=usuario)
            notificacionA.save()
            #Se obtienen los usuarios de todo el personal de todos los departamentos.
            usuariosDep = CustomUser.objects.exclude(departamento_id=None)
            #Registra la notificación de que la solicitud ha completado el proceso digital.
            for element in usuariosDep:
                notificacionB = Notificacion(solicitud_id=solicitud,
                                            descripcion="La solicitud " + solicitud + " ha sido rechazada por incumplimiento en la visita de la institución",
                                            leida='0',
                                            fechaNotificacion=datetime.datetime.now(),
                                            tipo_notificacion='P',
                                            usuario_id=element.id)
                notificacionB.save()
            return redirect('admin')

    else:
        return redirect('perfil')
