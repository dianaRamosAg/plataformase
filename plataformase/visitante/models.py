from django.db import models

# Create your models here.
class VisitanteSC(models.Model):
    first_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    password = models.TextField(blank=True, null=False)
    curp_rfc = models.CharField(max_length=18, blank=True, null=True)#Guarda la CURP o el RFC del usuario
    calle = models.TextField(blank=True, null=True)#
    noexterior = models.IntegerField(blank=True, null=True)
    nointerior = models.IntegerField(blank=True, null=True)
    codigopostal = models.IntegerField(blank=True, null=True)
    municipio = models.TextField(blank=True, null=True)
    colonia = models.TextField(blank=True, null=True)
    celular = models.TextField(blank=True, null=True)
    email = models.TextField(unique=True)
    leida = models.CharField(max_length=1, default='0',null=False)
    tipo_usuario = models.CharField(max_length=1, default='5')#1: Institución, 5: Particular
    tipo_persona = models.CharField(max_length=1, default='1')#1: Física, 2:Moral
    #Datos solo si son institución
    inst_cct = models.TextField(blank=True, null=True)
    inst_nombredirector = models.TextField(blank=True, null=True)
    sector = models.TextField(blank=True, null=True)  # Publico, Privado
    nivel_educativo = models.CharField(max_length=1, blank=True, null=True)  # 1: Media superior, 2: Superior, 3: Ambos
    modalidad = models.CharField(max_length=1, default='0',null=True) #1: Si es telebachillerato, 0:No
    
class ConfiguracionPDF(models.Model):
    nombre = models.TextField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    fondo = models.ImageField(upload_to ='formatoPDF/',blank=True,null=True) 