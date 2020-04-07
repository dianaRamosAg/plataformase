from django.db import models

# Create your models here.
class VisitanteSC(models.Model):
    pass
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
    tipo_usuario = models.CharField(max_length=1, default='4')#1: Institución, 2:jefe, 3:subordinado, 4:administrador
    tipo_persona = models.CharField(max_length=1, default='1')#1: Física, 2:Moral
    #Departamento al que pertenece el usuario (El modelo esta en aplicación usuarios)
    departamento = models.ForeignKey("RVOES.Departamento", on_delete=models.CASCADE, blank=True, null=True)
    jefe = models.CharField(max_length=1, default='0', blank=True, null=True)#Establece si es jefe o no (0: no, 1: si)
