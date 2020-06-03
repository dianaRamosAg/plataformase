from django.db import models
from .validators import valid_extension

class Departamento(models.Model):
    nombre = models.TextField()
    """ID= 1: Control Escolar, 2: Dirección, 3: Media Superior, 4: Superior"""

class Solicitud(models.Model):
    fechaRegistro = models.DateField(auto_now_add=False,)#Obtiene la fecha en la que se empezó el proceso de solicitud
    comentario = models.CharField(max_length=1, default='0',)#Indica si la solicitud tiene comentarios (0:no, 1:si, 2:ya actualizó archivos)
    nivel = models.CharField(max_length=1)#1: Media superior, 2: Superior
    modalidad = models.CharField(max_length=1)#1: Mixta, 2:Escolarizada 3:No escolarizada
    opcion = models.CharField(max_length=1)#Varía según la modalidad
    salud = models.CharField(max_length=1)#Indica si la solicitud es del área de la solicitud
    customuser = models.ForeignKey('login.CustomUser', on_delete=models.CASCADE,)#Usuario al que le pertenece la solicitud
    completado = models.IntegerField(default='1',)

    """completado: -1 = Cancelada, 0 = Completado, 1 = Institucional, 2 = Curricular,
    3 = Academica, 4 = Media Superior, 9 = Petición de pago, 10 = Documentos recibidos, 11 = Terminó revisión digital"""

    ciclonum = models.IntegerField(null=True, blank=True)
    ciclo = models.TextField(blank=True, null=True)
    otro = models.TextField(blank=True, null=True)
    duracion = models.FloatField(blank=True, null=True)
    nombre = models.TextField(blank=True, null=True, max_length=100)#Nombre de persona fisica
    apellidos = models.TextField(blank=True, null=True)
    libro_inscripcion = models.IntegerField(null=True, blank=True)
    fecha = models.DateField(null=True, blank=True)
    lugar = models.TextField(null=True, blank=True)
    objeto_social = models.TextField(blank=True, null=True)
    org_cop_acta = models.CharField(max_length=2, blank= True, null = True)
    identificacion = models.TextField(blank=True, null=True)
    org_cop_identificacion = models.CharField(max_length=2, blank= True, null = True)
    folio_id = models.TextField(null=True, blank=True)
    dom_particular = models.TextField(null=True, blank=True)
    celular = models.TextField(null=True, blank=True)
    curp_rfc = models.TextField(null=True, blank=True)
    email = models.TextField(null=True, blank=True)
    estatus = models.ForeignKey(Departamento, on_delete=models.CASCADE, default='1')
    """estatus: Define el departamnto en el que se encuentra"""
    noInstrumentoNotarial = models.IntegerField(blank=True, null=True)#Número de instrumento notarial
    nombreNotario = models.TextField(blank=True, null=True)#Nombre del notario público
    noNotario = models.IntegerField(blank=True, null=True)#Número de notario público
    nombreRepresentante = models.TextField(blank=True, null=True)#Nombre del representante legal
    nombreSolicitud = models.TextField(blank=True, null=True)#Nombre de la solicitud

    def __str__(self):
        return u'{0}'.format(self.id)
        #Cadena para representar el objeto solicitud (en el sitio de Admin, etc.)


class Notificacion(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)#Solicitud a la que corresponde la notificación
    descripcion = models.TextField(blank=True, null=True)#Mensaje de la notificación
    leida = models.CharField(max_length=1, blank=True, null=True)#Indica si ha sido leída (0:no, 1:sí)
    fechaNotificacion = models.DateField(auto_now_add=True)#Fecha en la que se generó la notificación
    tipo_notificacion = models.CharField(max_length=2, default='C')# H: Historial, C: Comentario, P: Personal administrativo
    #Usuario al que le pertenece la notificación.
    usuario = models.ForeignKey('login.CustomUser',
                                        on_delete=models.CASCADE, blank=True, null=True)

#Archivos para carpeta de Media Superior
class CMedSuperior(models.Model):
    #Solicitud a la que le pertenecen los archivos
    id_solicitud = models.ForeignKey('Solicitud',
                                    on_delete=models.CASCADE,)
    pago = models.FileField(upload_to='Archivos/MedSuperior', blank=True, null=True, validators=[valid_extension])#Ubicación de archivo de pago
    folio_pago = models.TextField(unique=True, default='0', blank=True, null=True)#Folio de pago no se puede repetir (incluido con los de superior)
    monto_pago = models.TextField(blank=True, null=True)#Monto de pago
    fecha_pago = models.DateField(blank=True, null=True, auto_now_add=False,)#Fecha en que se realizó el pagó
    #solicitud = models.FileField(upload_to='Archivos/MedSuperior', validators=[valid_extension])#Ubicación de archivo de solicitud
    identificacion = models.FileField(upload_to='Archivos/MedSuperior', validators=[valid_extension])#Ubicación de archivo de identificación oficial
    perDocente = models.FileField(upload_to='Archivos/MedSuperior', validators=[valid_extension])#Ubicación de archivo de personal docente
    instalaciones = models.FileField(upload_to='Archivos/MedSuperior', validators=[valid_extension])#Ubicación de archivo de Formato No. 6 "Instalaciones"
    dictamen_suelo = models.TextField(blank=True, null=True,)#Constancia de uso de suelo
    expediente_suelo = models.TextField(blank=True, null=True,)#Expediente de uso de suelo
    firma_suelo = models.TextField(blank=True, null=True,)#Nombre de quien firma la constancia de uso de suelo
    fecha_suelo = models.DateField(blank=True, null=True,)#Fecha que tiene el expediente de uso de suelo

    dictamen_estructural = models.TextField(blank=True, null=True,)#Nombre del dictamen estructural
    fecha_estructural = models.DateField(blank=True, null=True, auto_now_add=False,)#Fecha del dictamen estructural
    arqui_dictamen_estructural = models.TextField(blank=True, null=True,)#Nombre del responsable el dictamen estructural
    DRO_dictamen_estructural = models.TextField(blank=True, null=True,)#Director responsable de obra(DRO)
    noCedula_dictamen_estructural = models.TextField(blank=True, null=True,)#Número de cedula profesional

    dictamen_proteccion = models.TextField(blank=True, null=True,)#Folio de dictamen de protección civil
    fecha_dictamen_proteccion = models.DateField(blank=True, null=True, auto_now_add=False, )#Fecha de dictamen de protección civil
    firma_dictamen_proteccion = models.TextField(blank=True, null=True,)#Nombre de quien firma el dictamen de protección civil

    folio_inife = models.TextField(blank=True, null=True,)#Folio de dictamen de INIFE
    fecha_inife = models.DateField(blank=True, null=True, auto_now_add=False, )#Fecha de dictamen de INIFE
    firma_inife = models.TextField(blank=True, null=True,)#Nombre de quien firma el dictamen de INIFE
    #Si es virtual
    equipamiento = models.FileField(upload_to='Archivos/MedSuperior', blank=True, null=True, validators=[valid_extension])#Ubicación de archivo de formato no 7 tecnologia y equipamiento para la opción virtual
    progEstuio = models.FileField(upload_to='Archivos/MedSuperior', blank=True, null=True, validators=[valid_extension])#Ubicación de archivo de formato no 8 planes y programas de estudio
    #Si es del area de la salud
    cifrhs = models.FileField(upload_to='Archivos/Curricular', validators=[valid_extension], blank=True, null=True)#Ubicación de archivo de opinion favorable de CIFRHS
    carta = models.FileField(upload_to='Archivos/Curricular', validators=[valid_extension], blank=True, null=True)#Ubicación de archivo de carta de intención

    def __str__(self):
        return u'{0}'.format(self.id_solicitud)

#Archivos para carpeta Institucional
class CInstitucional(models.Model):
    #Solicitud a la que le pertenecen los archivos
    id_solicitud = models.ForeignKey('Solicitud',
                                    on_delete=models.CASCADE,)
    #solicitud = models.FileField(upload_to='Archivos/Institucional', validators=[valid_extension], blank=True, null=True)#Ubicación de archivo de solicitud
    folio_pago = models.TextField(unique=True, default='0', blank=True, null=True)#Folio de pago no se puede repetir (incluido con los de superior)
    monto_pago = models.TextField(blank=True, null=True)#Monto de pago
    fecha_pago = models.DateField(blank=True, null=True, auto_now_add=False,)#Fecha en que se realizó el pagó
    pago = models.FileField(upload_to='Archivos/Institucional', blank=True, null=True, validators=[valid_extension],)#Ubicación de archivo de pago
    acredita_personalidad = models.FileField(upload_to='Archivos/Institucional', validators=[valid_extension],)#Ubicación de archivo de documento que acredita personalidad juridica del particular
    acredita_inmueble = models.FileField(upload_to='Archivos/Institucional', validators=[valid_extension])#Ubicación de archivo de documento que acredita la ocupación legal del inmueble
    dictamen_suelo = models.TextField()#Constancia de uso de suelo
    expediente_suelo = models.TextField(blank=True, null=True,)#Expediente de uso de suelo
    firma_suelo = models.TextField(blank=True, null=True,)#Nombre de quien firma la constancia de uso de suelo
    fecha_suelo = models.DateField(blank=True, null=True,)#Fecha que tiene el expediente de uso de suelo
    licencia_suelo = models.FileField(upload_to='Archivos/Institucional', validators=[valid_extension],)#Ubicación de archivo de licencia de uso de suelo
    dictamen_estructural = models.TextField()#Nombre del dictamen estructural
    fecha_estructural = models.DateField(blank=True, null=True, auto_now_add=False,)#Fecha del dictamen estructural
    arqui_dictamen_estructural = models.TextField(blank=True, null=True,)#Nombre del responsable el dictamen estructural
    DRO_dictamen_estructural = models.TextField(blank=True, null=True,)#Director responsable de obra(DRO)
    noCedula_dictamen_estructural = models.TextField(blank=True, null=True,)#Número de cedula profesional
    constancia_estructural = models.FileField(upload_to='Archivos/Institucional', validators=[valid_extension])#Ubicación de archivo de constancia de seguridad estructural
    dictamen_proteccion = models.TextField(blank=True, null=True,)#Folio de dictamen de protección civil
    fecha_dictamen_proteccion = models.DateField(blank=True, null=True, auto_now_add=False, )#Fecha de dictamen de protección civil
    firma_dictamen_proteccion = models.TextField(blank=True, null=True,)#Nombre de quien firma el dictamen de protección civil
    constancia_proteccion = models.FileField(upload_to='Archivos/Institucional', validators=[valid_extension])#Ubicación de archivo de protección civil
    folio_inife = models.TextField()#Folio de dictamen de INIFE
    fecha_inife = models.DateField(blank=True, null=True, auto_now_add=False, )#Fecha de dictamen de INIFE
    firma_inife = models.TextField(blank=True, null=True,)#Nombre de quien firma el dictamen de INIFE
    inife = models.FileField(upload_to='Archivos/Institucional', validators=[valid_extension])#Ubicación de archivo de dictamen de INIFE
    des_instalacion = models.FileField(upload_to='Archivos/Institucional', validators=[valid_extension])#Ubicación de archivo de descripción de instalaciones
    planos = models.FileField(upload_to='Archivos/Institucional', validators=[valid_extension])#Ubicación de archivo de planos arquitectonicos y estructurales
    biblio = models.FileField(upload_to='Archivos/Institucional', validators=[valid_extension])#Ubicación de archivo de habilitada biblioteca de institución

    def __str__(self):
        return u'{0}'.format(self.id_solicitud)

#Archivos para carpeta Institucional
class CCurricular(models.Model):
    #Solicitud a la que le pertenecen los archivos
    id_solicitud = models.ForeignKey('Solicitud',
                                    on_delete=models.CASCADE,)
    estudio = models.FileField(upload_to='Archivos/Curricular', validators=[valid_extension])#Ubicación de archivo de estudio de factibilidad
    plan = models.FileField(upload_to='Archivos/Curricular', validators=[valid_extension])#Ubicación de archivo de plan de estudios
    mapa = models.FileField(upload_to='Archivos/Curricular', validators=[valid_extension])#Ubicación de archivo de mapa curricular
    programa = models.FileField(upload_to='Archivos/Curricular', validators=[valid_extension])#Ubicación de archivo de programas de estudio
    metodologia = models.FileField(upload_to='Archivos/Curricular', validators=[valid_extension], blank=True, null=True)#Ubicación de archivo de metodología de la modalidad
    cifrhs = models.FileField(upload_to='Archivos/Curricular', validators=[valid_extension], blank=True, null=True)#Ubicación de archivo de opinion favorable de CIFRHS
    carta = models.FileField(upload_to='Archivos/Curricular', validators=[valid_extension], blank=True, null=True)#Ubicación de archivo de carta de intención

    def __str__(self):
        return u'{0}'.format(self.id_solicitud)

#Archivos para carpeta Institucional
class CAcademica(models.Model):
    #Solicitud a la que le pertenecen los archivos
    id_solicitud = models.ForeignKey('Solicitud',
                                    on_delete=models.CASCADE,)
    rec_bibliograficos = models.FileField(upload_to='Archivos/Academica', validators=[valid_extension])#Ubicación de archivo de recursos bibliograficos existentes en la institución
    rec_didacticos = models.FileField(upload_to='Archivos/Academica', validators=[valid_extension])#Ubicación de archivo de recursos didacticos existentes en la institución
    talleres = models.FileField(upload_to='Archivos/Academica', validators=[valid_extension])#Ubicación de archivo de talleres
    apoyo_informatico = models.FileField(upload_to='Archivos/Academica', validators=[valid_extension])#Ubicación de archivo de infraestructura de apoyo informático
    apoyo_comunicaciones = models.FileField(upload_to='Archivos/Academica', validators=[valid_extension])#Ubicación de archivo de apoyo de comunicaciones
    personal = models.FileField(upload_to='Archivos/Academica', validators=[valid_extension])#Ubicación de archivo de relación del personal docente propuesto

    def __str__(self):
        return u'{0}'.format(self.id_solicitud)

class Comentarios(models.Model):
    #Solicitud a la que le pertenecen el comentario
    solicitud = models.ForeignKey(Solicitud,
                                   on_delete=models.CASCADE,)
    descripcion = models.TextField(blank=True, null=True)#Descripción de la observación realizada al documento
    fechaComentario = models.DateField(auto_now_add=True)#Fecha en que se realizó el comentario
    mostrado = models.CharField(max_length=1, blank=True, null=True,)#Identifica si el comentario ya se mostro a la institución (0:no, 1:sí)
    archivo = models.TextField(blank=True, null=True,)#Identifica a que archivo le corresponde el comentario (ver usuarios/views.py -> terminarSubArchivos)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, default='1')#Identifica que departamento realizó el comentario

class Actividades(models.Model):
    usuario = models.ForeignKey("login.CustomUser", on_delete=models.CASCADE)#Usuario que realizó la actividad
    descripcion = models.TextField()#Descripción de la actividad realizada
    fecha = models.DateField(auto_now=False, auto_now_add=False)#Fecha en que se realizó la actividad
    solicitud = models.ForeignKey('Solicitud', on_delete=models.CASCADE)#Solicitud a la que le pertenecen el comentario

class Acuerdos(models.Model):
    nombre = models.TextField(blank=True, null=True,)#Nombre del acuerdo
    archivo = models.FileField(upload_to='Archivos/Acuerdos',)#Ubicación del arcuerdo
    nivel = models.CharField(max_length=1,)#nivel 1: media superior, nivel 2: superior

class NotificacionRegistro(models.Model):
    email = models.TextField(blank=True, null=True)#Mensaje de la notificación
    nombres = models.TextField(blank=True, null=True)#Mensaje de la notificación
    curp = models.TextField(blank=True, null=True)#Mensaje de la notificación
    celular = models.TextField(blank=True, null=True)#Mensaje de la notificación
    leida = models.CharField(max_length=1, blank=True, null=True)#Indica si ha sido leída (0:no, 1:sí)
    fechaNotificacion = models.DateField(auto_now_add=True)#Fecha en la que se generó la notificación
    tipo_notificacion = models.CharField(max_length=2, default='C')# H: Historial, C: Comentario, P: Personal administrativo
    #Usuario al que le pertenece la notificación.
    usuario = models.ForeignKey('login.CustomUser',on_delete=models.CASCADE, blank=True, null=True)
    tipo_usuario = models.CharField(max_length=1, default='4')#1: Institución, 2:jefe, 3:subordinado, 4:administrador
