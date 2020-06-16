from django.db import models
from .validators import valid_extension

class Departamento(models.Model):
    nombre = models.TextField()
    """ID= 1: Control Escolar, 2: Dirección, 3: Media Superior, 4: Superior"""

class Solicitud(models.Model):
    fechaRegistro = models.DateField(auto_now_add=False,)#Obtiene la fecha en la que se empezó el proceso de solicitud
    comentario = models.CharField(max_length=1, default='0',)#Indica si la solicitud tiene comentarios (0:no, 1:si, 2:ya actualizó archivos)
    completado = models.IntegerField(default='1',)#Estado en el que se encuentra la solicitud
    """completado: -1 = Cancelada, 0 = Completado, 1 = Institucional, 2 = Curricular,
        3 = Academica, 4 = Media Superior, 9 = Petición de pago, 10 = Documentos recibidos, 11 = Nivel subio archivo,
        12 = Dirección aceptó/rechazo -> Fin del proceso (ir a Ventanilla única)"""
    estatus = models.ForeignKey(Departamento, on_delete=models.CASCADE, default='1')
    """estatus: Define el departamnto en el que se encuentra"""
    noOficioAdmision = models.TextField(null=True, blank=True, default=None)#Número de oficio de admisión de trámite
    archivoNivel = models.FileField(upload_to='Archivos/Archivos_Nivel', default='', blank=True, null=True, validators=[valid_extension])#Archivo que sube el nivel al finalizar la revisión de la solicitud en la segunda etapa del proceso (Revisión física)
    aceptArchivoNivel = models.BooleanField(default=False)#Indica si el archivo subido por el nivel fue aceptado (true) o rechazado (false)

    cct = models.TextField(null=True, blank=True)#Clave de Centro de Trabajo
    nivel = models.CharField(max_length=1)#Nivel Educativo (1: Media superior, 2: Superior)
    nivelSuperior = models.CharField(max_length=1, null=True, blank=True)#Nivel educativo especifico (Solo para nivel superior)
    modalidad = models.CharField(max_length=1)#Modalidad (1: Mixta, 2:Escolarizada 3:No escolarizada)
    opcion = models.CharField(max_length=1)#Opción (Varía según la modalidad)
    salud = models.CharField(max_length=1)#Indica si la solicitud es del área de la solicitud
    customuser = models.ForeignKey('login.CustomUser', on_delete=models.CASCADE,)#Usuario al que le pertenece la solicitud
    ciclonum = models.IntegerField(null=True, blank=True)
    ciclo = models.TextField(blank=True, null=True)
    otro = models.TextField(blank=True, null=True)
    duracion = models.FloatField(blank=True, null=True)
    #Ambos tipos de persona
    identificacion = models.TextField(blank=True, null=True)#Tipo de identificación oficial (Ambos)
    folio_id = models.TextField(null=True, blank=True)#Número de folio de identificación oficial (Ambos)
    #dom_particular = models.TextField(null=True, blank=True)#Domicilio legal del particular (Ambos). Quitado porque se obtendrá del registro del usuario
    #celular = models.TextField(null=True, blank=True)#Teléfono/Celular. Quitado porque se obtendrá del registro del usuario
    #curp_rfc = models.TextField(null=True, blank=True)#Registro Federal de Contribuyentes. Quitado porque se obtendrá del registro del usuario
    #email = models.TextField(null=True, blank=True)#Correo electrónico para recibir notificaciones. Quitado porque se obtendrá del registro del usuario

    #Personas autorizadas por el particular
    nomPerAut1 = models.TextField(blank=True, null=True)#Nombre (Persona 1)
    apMatPerAut1 = models.TextField(blank=True, null=True)#Apellido Materno (Persona 1)
    apPatPerAut1 = models.TextField(blank=True, null=True)#Apellido Paterno (Persona 1)
    emailPerAut1 = models.TextField(blank=True, null=True)#Email (Persona 1)
    telPerAut1 = models.TextField(blank=True, null=True)#Teléfono de contacto (Persona 1)

    nomPerAut2 = models.TextField(blank=True, null=True)#Nombre (Persona 2)
    apMatPerAut2 = models.TextField(blank=True, null=True)#Apellido Materno (Persona 2)
    apPatPerAut2 = models.TextField(blank=True, null=True)#Apellido Paterno (Persona 2)
    emailPerAut2 = models.TextField(blank=True, null=True)#Email (Persona 2)
    telPerAut2 = models.TextField(blank=True, null=True)#Teléfono de contacto (Persona 2)

    nomPerAut3 = models.TextField(blank=True, null=True)#Nombre (Persona 3)
    apMatPerAut3 = models.TextField(blank=True, null=True)#Apellido Materno (Persona 3)
    apPatPerAut3 = models.TextField(blank=True, null=True)#Apellido Paterno (Persona 3)
    emailPerAut3 = models.TextField(blank=True, null=True)#Email (Persona 3)
    telPerAut3 = models.TextField(blank=True, null=True)#Teléfono de contacto (Persona 3)

    nomPerAut4 = models.TextField(blank=True, null=True)#Nombre (Persona 4)
    apMatPerAut4 = models.TextField(blank=True, null=True)#Apellido Materno (Persona 4)
    apPatPerAut4 = models.TextField(blank=True, null=True)#Apellido Paterno (Persona 4)
    emailPerAut4 = models.TextField(blank=True, null=True)#Email (Persona 4)
    telPerAut4 = models.TextField(blank=True, null=True)#Teléfono de contacto (Persona 4)

    nomPerAut5 = models.TextField(blank=True, null=True)#Nombre (Persona 5)
    apMatPerAut5 = models.TextField(blank=True, null=True)#Apellido Materno (Persona 5)
    apPatPerAut5 = models.TextField(blank=True, null=True)#Apellido Paterno (Persona 5)
    emailPerAut5 = models.TextField(blank=True, null=True)#Email (Persona 5)
    telPerAut5 = models.TextField(blank=True, null=True)#Teléfono de contacto (Persona 5)

    nomPerAut6 = models.TextField(blank=True, null=True)#Nombre (Persona 6)
    apMatPerAut6 = models.TextField(blank=True, null=True)#Apellido Materno (Persona 6)
    apPatPerAut6 = models.TextField(blank=True, null=True)#Apellido Paterno (Persona 6)
    emailPerAut6 = models.TextField(blank=True, null=True)#Email (Persona 6)
    telPerAut6 = models.TextField(blank=True, null=True)#Teléfono de contacto (Persona 6)

    #Apoderados legales
    nomApLegal1 = models.TextField(blank=True, null=True)#Nombre (Persona 1)
    apMatApLegal1 = models.TextField(blank=True, null=True)#Apellido Materno (Persona 1)
    apPatApLegal1 = models.TextField(blank=True, null=True)#Apellido Paterno (Persona 1)
    emailApLegal1 = models.TextField(blank=True, null=True)#Email (Persona 1)
    telApLegal1 = models.TextField(blank=True, null=True)#Teléfono de contacto (Persona 1)
    poderNotApLegal1 = models.TextField(blank=True, null=True)#Datos del poder notarial (Persona 1)

    nomApLegal2 = models.TextField(blank=True, null=True)#Nombre (Persona 2)
    apMatApLegal2 = models.TextField(blank=True, null=True)#Apellido Materno (Persona 2)
    apPatApLegal2 = models.TextField(blank=True, null=True)#Apellido Paterno (Persona 2)
    emailApLegal2 = models.TextField(blank=True, null=True)#Email (Persona 2)
    telApLegal2 = models.TextField(blank=True, null=True)#Teléfono de contacto (Persona 2)
    poderNotApLegal2 = models.TextField(blank=True, null=True)#Datos del poder notarial (Persona 2)

    perPrograma = models.CharField(max_length=1, null=True, blank=True)#Pertenencia al programa de mejora institucional
    nombreSolicitud = models.TextField(blank=True, null=True)#Nombre completo del plan y programas de estudio
    #Denominación de la institución y del Plantel en que se impartirá (Solo para particulares)
    opcion1 = models.TextField(blank=True, null=True)# Opción 1
    opcion2 = models.TextField(blank=True, null=True)# Opción 2
    opcion3 = models.TextField(blank=True, null=True)# Opción 3
    horarioDias = models.TextField(blank=True, null=True)# Horiario y días en que lo impartirá
    areaFormacion = models.TextField(blank=True, null=True)#Área o campo de formación

    #Departamentos
    org_cop_identificacion = models.BooleanField(blank= True, null = True)#¿Presenta original y copia...? (para los departamentos)
    org_cop_acta = models.BooleanField(blank= True, null = True)

    #Persona Moral
    noInstrumentoNotarial = models.IntegerField(blank=True, null=True)#Número de instrumento notarial (inst_notarial en plantilla)
    libro_inscripcion = models.TextField(null=True, blank=True)#Número de Libro de inscripción
    nombreNotario = models.TextField(blank=True, null=True)#Nombre del notario público
    noNotario = models.IntegerField(blank=True, null=True)#Número de notario público
    fecha = models.DateField(null=True, blank=True)#Fecha de expedición
    lugar = models.TextField(null=True, blank=True)#Lugar de expedición
    objeto_social = models.TextField(blank=True, null=True)#Duración y objeto social
    estatutosVigentes = models.TextField(blank=True, null=True)#Datos de estatutos vigente
    nombreRepresentante = models.TextField(blank=True, null=True)#Nombre del representante legal
    poderNotarial = models.TextField(blank=True, null=True)#Datos del poder notarial del representante legal

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
    solicitud = models.FileField(upload_to='Archivos/MedSuperior', validators=[valid_extension], default="")#Ubicación de archivo de solicitud
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
    solicitud = models.FileField(upload_to='Archivos/Institucional', validators=[valid_extension], blank=True, null=True, default="")#Ubicación de archivo de solicitud
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
    atendida = models.BooleanField(default=False)

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
    tipo_usuario = models.CharField(max_length=1, default='4')#1: