# login/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

#Modelo de personalización de usuarios
class CustomUser(AbstractUser):
    #Para conservar los valores que ya tiene por defecto el modelo de usuarios.
    pass
    curp_rfc = models.CharField(max_length=18, blank=True, null=True)#Guarda la CURP o el RFC del usuario
    calle = models.TextField(blank=True, null=True)#
    noexterior = models.IntegerField(blank=True, null=True)
    nointerior = models.IntegerField(blank=True, null=True)
    codigopostal = models.IntegerField(blank=True, null=True)
    municipio = models.TextField(blank=True, null=True)
    colonia = models.TextField(blank=True, null=True)
    celular = models.TextField(blank=True, null=True)
    tipo_usuario = models.CharField(max_length=1, default='4')#1: Institución, 2:jefe, 3:subordinado, 4:administrador
    tipo_persona = models.CharField(max_length=1, default='1')#1: Física, 2:Moral
    #Departamento al que pertenece el usuario (El modelo esta en aplicación usuarios)
    departamento = models.ForeignKey("RVOES.Departamento", on_delete=models.CASCADE, blank=True, null=True)
    jefe = models.CharField(max_length=1, default='0', blank=True, null=True)#Establece si es jefe o no (0: no, 1: si)
    registro = models.ForeignKey("CustomUser", on_delete=models.CASCADE, blank=True, null=True)#Usuario que registro a este usuario
    firma_digital = models.FileField(upload_to ='firmas_digitales/', blank=True, null=True)
    localidad = models.TextField(blank=True, null=True)
    #Campo que funciona por defecto como email
    #USERNAME_FIELD = 'username'
    #Campos requeridos para la creación de usuario (principalmente para el usuario root)
    REQUIRED_FIELDS = [ 'first_name','password','email']

    def __str__(self):
        """Este método define como se muestra por defecto el usuario.

        Parámetros
        -:param self: Instancia de CustomUser

        Retorna
        -:return: Retorna el nombre y apellido el usuario
        """
        return self.first_name , self.last_name


class UsuarioInstitucion(models.Model):
    id_usuariobase = models.ForeignKey("CustomUser", on_delete=models.CASCADE, blank=True, null=True)#Institución a la que pertenece el registro
    cct = models.TextField(blank=True, null=True, unique=True)#Clave de centro de trabajo
    nombredirector = models.TextField(blank=True, null=True)#Nombre del director del centro del trabajo
    sector = models.TextField(blank=True, null=True)#Publico, Privado
    is_active = models.BooleanField(blank=True, null=True, default=True)#Es una institución activa
    nivel_educativo = models.CharField(max_length=1, blank=True, null=True)#1: Media superior, 2: Superior, 3: Ambos
    modalidad = models.CharField(max_length=1, default='0',null=True) #1: Si es telebachillerato, 0:No