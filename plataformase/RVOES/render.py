import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from login.models import CustomUser
from .models import Solicitud, Departamento, CMedSuperior, CInstitucional, Notificacion
from django.utils import timezone

#pass_db = "12345"
pass_db = "ismael"

def link_callback(uri, rel):
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    #Convertir URI en rutas absolutas del sistema
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  #Manejar uri absoluta (es decir: http: //some.tld/foo.png)

    #Asegúrese de que ese archivo existe
    if not os.path.isfile(path):
            raise Exception('media URI must start with %s or %s' % (sUrl, mUrl))
    return path

def render_pdf_planes_prog_estud(request, id):
    """Genera el archivo PDF de Planes y Programas de Estudio

    Parámetros
    -:param request: Contiene información del navegador del usuario que está realizando la petición.
    -:param request: Contiene el id de la solicitud a la que se le quiere generar el PDF.

    Retorna
    -:return HttpResponse: Regresa que se tiene un error.
    -:return response: Regresa el archivo PDF, lo descarga automáticamente.
    """
    #Definimos el archivo PDF que vamos a utilizar como plantilla
    template_path = 'PDF - Planes y Programas de Estudio.html'
    #Obtenemos la fecha actual
    today = timezone.now()
    #Obtenemos la solicitud a la que se quiere generar el PDF
    solicitud = Solicitud.objects.get(id=id)
    #Obtenemos los datos del jefe del departamento.
    jefe = CustomUser.objects.filter(departamento_id=int(solicitud.estatus.id))
    #Obtenemos el nombre del departamento
    departamento = Departamento.objects.filter(id=solicitud.estatus.id)
    #Obtiene la fecha de cuando la solicitud salió de dirección
    fecha = obtenerFecha(id)
    #Si la solicitud es de media superior
    if solicitud.nivel == '1':
        nivel = "Media Superior"
        #Obtenemos los datos de la carpeta de media superior
        datos = CMedSuperior.objects.get(id_solicitud=id)
        #Obenemos la modalidad y su opción
        if solicitud.modalidad == '1':
            mod = 'MIXTA'
            if solicitud.opcion == '1':
                opc = 'MIXTA'
            if solicitud.opcion == '2':
                opc = 'AUTO-PLANEADA'
        if solicitud.modalidad == '2':
            mod = 'ESCOLARIZADA'
            if solicitud.opcion == '1':
                opc = 'INTENSIVA'
            if solicitud.opcion == '2':
                opc = 'PRESENCIAL'
        if solicitud.modalidad == '3':
            mod = 'NO ESCOLARIZADA'
            if solicitud.opcion == '1':
                opc = 'CERTIFICACIÓN POR EVALUACIONES PARCIALES'
            if solicitud.opcion == '2':
                opc = 'VIRTUAL'
    else:
        nivel = "Superior"
        #Obtenemos los datos de la carpeta institucional
        datos = CInstitucional.objects.get(id_solicitud=id)
        #Obenemos la modalidad y su opción
        if solicitud.modalidad == '1':
            mod = 'MIXTA'
            if solicitud.opcion == '1':
                opc = 'DUAL'
            if solicitud.opcion == '2':
                opc = 'ABIERTA / DISTANCIA'
            if solicitud.opcion == '3':
                opc = 'EN LINEA / VIRUAL'
        if solicitud.modalidad == '2':
            mod = 'ESCOLARIZADA'
            if solicitud.opcion == '1':
                opc = 'PRESENCIAL'
        if solicitud.modalidad == '3':
            mod = 'NO ESCOLARIZADA'
            if solicitud.opcion == '1':
                opc = 'CERTIFICACIÓN POR EXAMEN'
            if solicitud.opcion == '2':
                opc = 'ABIERTA / DISTANCIA'
            if solicitud.opcion == '3':
                opc = 'EN LINEA / VIRUAL'
    #Creamos una variable donde se guardarán todas la variables
    #usuario =solicitud.customuser.id
    context = {
        'today': today,
        'solicitud': solicitud,
        'jefe': jefe,
        'departamento': departamento,
        'fecha': fecha,
        'datos': datos,
        'mod': mod,
        'opc': opc,
        #'usuario': usuario,
        'nivel': nivel,
    }
    #Cree un objeto de respuesta Django y especifique content_type como pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Admisión de trámite.pdf"'
    #Encuentre la plantilla y renderícela.
    template = get_template(template_path)
    html = template.render(context)
    #Creamos el PDF
    pisaStatus = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    #Si hay errores muestra el mensaje.
    if pisaStatus.err:
       return HttpResponse('Tenemos algunos errores :( <pre>' + html + '</pre>')
    return response

#Obtener fecha de cuando la solicitud salio de dirección
def obtenerFecha(id_solicitud):
    #nivel = Solicitud.objects.values_list('nivel').filter(id=id_solicitud)[0]
    id_jefe = CustomUser.objects.get(jefe='1', departamento=2)
    record = Notificacion.objects.get(solicitud_id=id_solicitud,
                                      descripcion = "Esta solicitud esta pendiente de visita de revisión",
                                      usuario_id = id_jefe)
    print("record ->",record.fechaNotificacion)
    return record.fechaNotificacion
    # import psycopg2
    # try:
    #     connection = psycopg2.connect(user="postgres", password=pass_db, host="localhost", port="5432",
    #                                   database="RVOES")
    #     cursor = connection.cursor()
    #     select = "SELECT \"fechaNotificacion\" " \
    #         "FROM usuarios_notificacion " \
    #         "WHERE solicitud_id = %s " \
    #         "AND descripcion = 'Una solicitud pasó a ser revisada por tú área' " \
    #         "AND usuario_id IN " \
    #             "(SELECT id " \
    #             "FROM login_customuser " \
    #             "WHERE departamento_id = 2 AND jefe = '1');"
    #     cursor.execute(select, (id_solicitud,))
    #     record = cursor.fetchone()
    #     cursor.close()
    #     connection.close()
    #     solicitud = Solicitud.objects.
    #     record = CustomUser.objects.values_list('id').
    #     return record[0]
    # except (Exception, psycopg2.Error) as error:
    #     print("Error al obtener datos con el método obtenerFecha", error)
