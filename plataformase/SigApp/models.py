from django.db import models

#A todos los campos que son llaves foraneas en las tablas Django les agregó '_id' al final: NombreCampoEjemplo_id

class CentroTrabajo(models.Model):
    Clave_CentroTrabajo = models.CharField(primary_key=True,max_length=30)
    Nombre_CentroTrabajo = models.CharField(max_length=100)
    Descripcion = models.CharField(max_length=200)

class Institucion(models.Model):
    Clave_Institucion  = models.CharField(primary_key=True,max_length=30)
    Nombre_Institucion = models.CharField(max_length=100)
    estatus = models.CharField(max_length=15)
    Clave_CentroTrabajo = models.ForeignKey(CentroTrabajo,on_delete=models.CASCADE)
    Dominio_Institucion = models.CharField(max_length=7)
    totalDocentes = models.BigIntegerField()
    totalAdministrativos = models.BigIntegerField()
    Director_Institucion = models.CharField(max_length=100)
    ImagenNo1 = models.ImageField(upload_to='imagenes_instituciones_perfil',blank=True,null=True)
    ImagenNo2 = models.ImageField(upload_to='imagenes_instituciones_perfil',blank=True,null=True)
    ImagenNo3 = models.ImageField(upload_to='imagenes_instituciones_perfil',blank=True,null=True)

class Escuela(models.Model):
    IdEscuela = models.CharField(primary_key=True, max_length=30)
    NombreEscuela = models.CharField(max_length=50)
    RazonSocial = models.CharField(max_length=50)
    Dominio = models.CharField(max_length=50)
    Personal = models.CharField(max_length=50)
    CodPostal = models.CharField(max_length=50)
    ClaveM = models.CharField(max_length=50)
    Municipio = models.CharField(max_length=50)
    ClaveL = models.CharField(max_length=50)
    Localidad = models.CharField(max_length=50)
    Latitud = models.CharField(max_length=50)
    Longitud = models.CharField(max_length=50)

class AreaInteres(models.Model):
    Clave_Area = models.AutoField(primary_key=True)
    Descripcion = models.CharField(max_length=30)

class Carrera(models.Model):
    Clave_Carrera = models.AutoField(primary_key=True)
    Nombre_Carrera = models.CharField(max_length=50)
    areaInteres = models.ForeignKey(AreaInteres,on_delete=models.CASCADE)


class DetalleCarrera(models.Model):
    Clave_Carrera = models.ForeignKey(Carrera,on_delete=models.CASCADE)
    Clave_Institucion = models.ForeignKey(Institucion,on_delete=models.CASCADE)
    Descripcion = models.CharField(max_length=200)


class Periodos(models.Model):
    Clave_Periodo = models.AutoField(primary_key=True)
    Descripcion = models.CharField(max_length=20)

class GradoAcademico(models.Model):
    Clave_GradoAcademico = models.AutoField(primary_key=True)
    Descripcion = models.CharField(max_length=25)

class Modalidad(models.Model):
    Clave_Modalidad = models.AutoField(primary_key=True)
    Descripcion = models.CharField(max_length=20)

class Municipio(models.Model):
    Clave_Municipio = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=30)

class Localidad(models.Model):
    Clave_Localidad = models.AutoField(primary_key=True)
    Clave_Municipio = models.ForeignKey(Municipio,on_delete=models.CASCADE)
    Nombre = models.CharField(max_length=70)

class UbicacionCentroTrabajo(models.Model):
    #Cuando se quiere usar una llave foranea como primaria Django recomienda utilizar models.OneToOneField
    Clave_CentroTrabajo = models.OneToOneField(CentroTrabajo,on_delete=models.CASCADE,primary_key=True)
    #Localidad = models.CharField(max_length=50)
    Localidad = models.ForeignKey(Localidad,on_delete=models.CASCADE)
    direccion = models.CharField(max_length=250)

class RVOE(models.Model):
    IdRVOE = models.CharField(max_length=30,primary_key=True)
    Clave_Institucion = models.ForeignKey(Institucion,on_delete=models.CASCADE)
    Clave_Carrera = models.ForeignKey(Carrera,on_delete=models.CASCADE)
    Clave_Periodo = models.ForeignKey(Periodos,on_delete=models.CASCADE)
    Clave_Modalidad = models.ForeignKey(Modalidad,on_delete=models.CASCADE)
    Clave_GradoAcademico = models.ForeignKey(GradoAcademico,on_delete=models.CASCADE)

class DatosEstadisticos(models.Model):
    FechaRegistro = models.DateTimeField(primary_key=True)
    IdRVOE = models.ForeignKey(RVOE,on_delete=models.CASCADE)
    totalAlumnos = models.BigIntegerField()
    totalAlumnosFemenino = models.BigIntegerField()
    totalAlumnosMasculino = models.BigIntegerField()
    totalAlumnosIndigenas = models.BigIntegerField()
    alumnosIndigenasM = models.BigIntegerField()
    alumnosIndigenasF =models.BigIntegerField()

    alumnosPrimerGrado = models.IntegerField()
    AlumnosIndigenasPrimerGrado = models.BigIntegerField()
    alumnosPrimerGradoHombres = models.IntegerField()
    alumnosPrimerGradoMujeres = models.IntegerField()
    alumnosIPrimerGradoHombres = models.IntegerField()
    alumnosIPrimerGradoMujeres = models.IntegerField()

    alumnosSegundoGrado = models.IntegerField()
    AlumnosIndigenasSegundoGrado = models.BigIntegerField()
    alumnosSegundoGradoHombres = models.IntegerField()
    alumnosSegundoGradoMujeres = models.IntegerField()
    alumnosISegundoGradoHombres = models.IntegerField()
    alumnosISegundoGradoMujeres = models.IntegerField()

    alumnosTercerGrado = models.IntegerField()
    AlumnosIndigenasTercerGrado = models.BigIntegerField()
    alumnosTercerGradoHombres = models.IntegerField()
    alumnosTercerGradoMujeres = models.IntegerField()
    alumnosITercerGradoHombres = models.IntegerField()
    alumnosITercerGradoMujeres = models.IntegerField()

    alumnosCuartoGrado = models.IntegerField()
    AlumnosIndigenasCuartoGrado = models.BigIntegerField()
    alumnosCuartoGradoHombres = models.IntegerField()
    alumnosCuartoGradoMujeres = models.IntegerField()
    alumnosICuartoGradoHombres = models.IntegerField()
    alumnosICuartoGradoMujeres = models.IntegerField()

    alumnosQuintoGrado = models.IntegerField()
    AlumnosIndigenasQuintoGrado = models.BigIntegerField()
    alumnosQuintoGradoHombres = models.IntegerField()
    alumnosQuintoGradoMujeres = models.IntegerField()
    alumnosIQuintoGradoHombres = models.IntegerField()
    alumnosIQuintoGradoMujeres = models.IntegerField()

    alumnosSextoGrado = models.IntegerField()
    AlumnosIndigenasSextoGrado = models.BigIntegerField()
    alumnosSextoGradoHombres = models.IntegerField()
    alumnosSextoGradoMujeres = models.IntegerField()
    alumnosISextoGradoHombres = models.IntegerField()
    alumnosISextoGradoMujeres = models.IntegerField()

class DatosTemporal(models.Model):
    clave_centrotrabajo_temp = models.CharField(max_length=200)
    direccion_temp = models.CharField(max_length=200)
    director_temp = models.CharField(max_length=200)
    nombre_institucion = models.CharField(max_length=200)
    municipio = models.CharField(max_length=200)
    localidad =   models.CharField(max_length=200)
    usuario_mod = models.CharField(max_length=150,blank=True,null=True)
    status = models.CharField(max_length=200)
    latitud_temp = models.CharField(max_length=200, null=True) ##
    longitud_temp = models.CharField(max_length=200, null=True ) ##
    modificando = models.BooleanField()

class HistorialMod(models.Model):
    fechamod = models.DateTimeField()
    departamento = models.CharField(max_length=50, blank=True, null=True)
    usuario_dep = models.CharField(max_length=200)
    usuario_mod = models.CharField(max_length=200)
    tipo = models.BooleanField(blank=True, null=True) #True = Aceptada
    comentario = models.CharField(max_length=500, blank=True, null=True)
    #
    clave_centrotrabajo_prev = models.CharField(max_length=200)
    direccion_prev = models.CharField(max_length=200)
    director_prev = models.CharField(max_length=200)
    nombre_institucion_prev = models.CharField(max_length=200)
    municipio_prev = models.CharField(max_length=200)
    localidad_prev = models.CharField(max_length=200)
    latitud_prev = models.CharField(max_length=200, null=True) ##
    longitud_prev = models.CharField(max_length=200, null=True) ##
    status_prev = models.CharField(max_length=200)
    #
    clave_centrotrabajo_new = models.CharField(max_length=200)
    direccion_new = models.CharField(max_length=200)
    director_new = models.CharField(max_length=200)
    nombre_institucion_new = models.CharField(max_length=200)
    municipio_new = models.CharField(max_length=200)
    localidad_new = models.CharField(max_length=200)
    latitud_new = models.CharField(max_length=200, null=True) ##
    longitud_new = models.CharField(max_length=200, null=True) ##
    status_new = models.CharField(max_length=200)


#Modelo para catalogo
class EscuelaC(models.Model):
    ClaveEscuela = models.CharField(primary_key=True, max_length=200)
    NombreEscuela = models.CharField(max_length=200)
    EstatusEscuela = models.CharField(max_length=200)
    Calle = models.CharField(max_length=200)
    Municipio = models.CharField(max_length=200)
    Localidad = models.CharField(max_length=200)
    CodPostal = models.CharField(max_length=200)
    Latitud = models.CharField(max_length=200)
    Longitud = models.CharField(max_length=200)
    Dominio = models.CharField(max_length=200)
    nombreDirector = models.CharField(max_length=200)
    ApellidoP_Director = models.CharField(max_length=200)
    ApellidoM_Director = models.CharField(max_length=200)
    Telefono_Director = models.CharField(max_length=200)
    Celuar_Director = models.CharField(max_length=200)
    Email = models.CharField(max_length=200) 
    Nivel = models.CharField(max_length=200)
    TipoServicio = models.CharField(max_length=200)
    ImagenNo1 = models.ImageField(upload_to='imagenes_instituciones_perfil',blank=True,null=True)
    ImagenNo2 = models.ImageField(upload_to='imagenes_instituciones_perfil',blank=True,null=True)
    ImagenNo3 = models.ImageField(upload_to='imagenes_instituciones_perfil',blank=True,null=True)
    
    
class estadisticosNuevo(models.Model):
    ClaveEscuela = models.ForeignKey(EscuelaC,on_delete=models.CASCADE,unique=True)
    TotalAlumnos = models.IntegerField()
    TotalPrimero = models.IntegerField()
    TotalSegundo = models.IntegerField()
    TotalTercero = models.IntegerField()
    TotalCuarto = models.IntegerField()
    TotalQuinto = models.IntegerField()
    TotalSexto = models.IntegerField()
    TotalHombres = models.IntegerField()
    TotalMujeres = models.IntegerField()
    
class RVOES(models.Model):
    ClaveEscuela = models.ForeignKey(EscuelaC,on_delete=models.CASCADE)
    NombreCarrera = models.CharField(max_length=200)
    TotalAlumnos = models.IntegerField()
    TotalPrimero = models.IntegerField()
    TotalSegundo = models.IntegerField()
    TotalTercero = models.IntegerField()
    TotalCuarto = models.IntegerField()
    TotalQuinto = models.IntegerField()
    TotalSexto = models.IntegerField()
    TotalHombres = models.IntegerField()
    TotalMujeres = models.IntegerField()
    Tipo = models.CharField(max_length=50)
    Area = models.CharField(max_length=100)
    ClaveCarrera = models.CharField(max_length=30)
    Modalidad = models.CharField(max_length=25)
    Periodos = models.CharField(max_length=25)
    modificando = models.BooleanField(default=False)



class HistorialModEstadistica(models.Model):
    fechamod = models.DateTimeField()

    tipo = models.BooleanField(blank=True, null=True) #True = Aceptada
    comentario = models.CharField(max_length=500, blank=True, null=True)
    usuario_dep = models.CharField(max_length=200)
    usuario_mod = models.CharField(max_length=200)
    departamento = models.CharField(max_length=50, blank=True, null=True)

    ClaveEscuela_prev = models.CharField(max_length=200)
    ClaveCarrera_prev = models.CharField(max_length=30)
    NombreCarrera_prev = models.CharField(max_length=200)

    TotalAlumnos_prev = models.IntegerField(blank=True, null=True)
    TotalPrimero_prev = models.IntegerField()
    TotalSegundo_prev = models.IntegerField()
    TotalTercero_prev = models.IntegerField()
    TotalCuarto_prev = models.IntegerField()
    TotalQuinto_prev = models.IntegerField()
    TotalSexto_prev = models.IntegerField()
    TotalHombres_prev = models.IntegerField()
    TotalMujeres_prev = models.IntegerField()
    Tipo_prev = models.CharField(max_length=50)
    Area_prev = models.CharField(max_length=100, blank=True, null=True)
    Modalidad_prev = models.CharField(max_length=25)
    Periodos_prev = models.CharField(max_length=25)
    #
    ClaveEscuela_new = models.CharField(max_length=200)
    ClaveCarrera_new = models.CharField(max_length=30)
    NombreCarrera_new = models.CharField(max_length=200)

    TotalAlumnos_new = models.IntegerField(blank=True, null=True)
    TotalPrimero_new = models.IntegerField()
    TotalSegundo_new = models.IntegerField()
    TotalTercero_new = models.IntegerField()
    TotalCuarto_new = models.IntegerField()
    TotalQuinto_new = models.IntegerField()
    TotalSexto_new = models.IntegerField()
    TotalHombres_new = models.IntegerField()
    TotalMujeres_new = models.IntegerField()
    Tipo_new = models.CharField(max_length=50)
    Area_new = models.CharField(max_length=100, blank=True, null=True)
    Modalidad_new = models.CharField(max_length=25)
    Periodos_new = models.CharField(max_length=25)

class DatosTemporalEstadistica(models.Model):
    ClaveEscuela_temp = models.CharField(max_length=200)
    NombreCarrera_temp = models.CharField(max_length=200)
    TotalPrimero_temp = models.IntegerField()
    TotalSegundo_temp = models.IntegerField()
    TotalTercero_temp = models.IntegerField()
    TotalCuarto_temp = models.IntegerField()
    TotalQuinto_temp = models.IntegerField()
    TotalSexto_temp = models.IntegerField()
    TotalHombres_temp = models.IntegerField()
    TotalMujeres_temp = models.IntegerField()
    Tipo_temp = models.CharField(max_length=50)
    Area_temp = models.CharField(max_length=100, blank=True, null=True)
    ClaveCarrera_temp = models.CharField(max_length=30)
    Modalidad_temp = models.CharField(max_length=25)
    Periodos_temp = models.CharField(max_length=25)
    usuario_mod = models.CharField(max_length=150, blank=True,null=True)
    modificando = models.BooleanField()
