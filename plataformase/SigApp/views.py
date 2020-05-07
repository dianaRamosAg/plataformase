from django.http import HttpResponse
from django.shortcuts import render
from .models import GradoAcademico, AreaInteres, Municipio,Localidad, Institucion,CentroTrabajo,UbicacionCentroTrabajo,DetalleCarrera,Carrera,RVOE,DatosEstadisticos,Modalidad,Periodos, Escuela, DatosTemporal, EscuelaC, estadisticosNuevo,RVOES
from django.db.models import OuterRef, Subquery, Sum
from django.core import serializers
from django.urls import reverse
from django.http import JsonResponse
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from .forms import ImagenesInstitucion
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.db.models import Q

# migracion excel bd : COPY "SigApp_localidad" ("Nombre","Clave_Municipio_id") FROM 'C:\4.csv' DELIMITER ',' CSV HEADER  encoding 'windows-1251';
def index(request):
    GradosAcademicos = GradoAcademico.objects.all()
    instituciones = EscuelaC.objects.all()

    Localidades = Localidad.objects.all()

    AreasIntereses = AreaInteres.objects.all()
    Municipios = Municipio.objects.all()
    return render(request,'SigApp/index.html',{
        "opcionesinstituciones": instituciones,

        "opcionesgrados": GradosAcademicos,
        "areaseducacion":AreasIntereses,
        "opcionesmunicipios": Municipios,
        "localidades": Localidades,

    })

def selecccion_municipio(request,mun):
    stackLocalidades = serializers.serialize("json",Localidad.objects.filter(Clave_Municipio__pk=mun))
    return JsonResponse(stackLocalidades,safe=False)

def localizador(request):
    GradosAcademicos = GradoAcademico.objects.all()
    Localidades = Localidad.objects.all()
    AreasIntereses = AreaInteres.objects.all()
    Municipios = Municipio.objects.all()
    Escuelas = EscuelaC.objects.all()
    return render(request,'SigApp/mapa_instituciones.html',{
        "opcionesgrados": GradosAcademicos,
        "areaseducacion":AreasIntereses,
        "opcionesmunicipios": Municipios,
        "localidades": Localidades,
        "coordenadas": Escuelas,
    })

def updInfo(request,Ndirector,Ninstitucion):
    nombre = Ninstitucion.replace("-"," ")
    director = Ndirector.replace("-"," ")
    EscuelaC.objects.filter(NombreEscuela=nombre).update(nombreDirector=director)
    result = {'Resultado': 'Prueba del resultado'}
    return JsonResponse(result)

def updInst(request,municipio,localidad,nivelacademico,areainteres,dominio): 
    municipio=municipio.replace('-',' ')   
    if municipio != 'empty':
        if(municipio=='RUIZ'):
            municipio='RUÍZ'
        if(municipio=='AHUACATLAN'):
            municipio='AHUACATLÁN'
        if(municipio=='AMATLAN DE CANAS'):
            municipio='AMATLÁN DE CAÑAS'
        if(municipio=='IXTLAN DEL RIO'):
            municipio='IXTLÁN DEL RÍO'
        if(municipio=='SANTA MARIA DEL ORO'):
            municipio='SANTA MARÍA DEL ORO'
        if(municipio=='BAHIA DE BANDERAS'):
            municipio='BAHÍA DE BANDERAS'
        municipio=municipio.replace("-"," ")
    if localidad != 'empty':
        localidad=localidad.replace("-"," ") 
    if nivelacademico != 'empty':
        nivelacademico=nivelacademico.replace("-"," ")  
    if dominio != 'empty':
        if dominio == 'PUBLICO':
           dominio = 'PÚBLICO'#Acento u
        if areainteres != 'empty': 
            if nivelacademico != 'empty':
                if municipio != 'empty':
                    if localidad != 'empty':
                        #Si hay una localidad seleccionada se filtará por localidad,Sector,Area de Interes y Nivel Academico
                        # Reemplazar filtro InstitucionesFiltradas = serializers.serialize("json",Institucion.objects.filter(Clave_CentroTrabajo__in=Subquery(UbicacionCentroTrabajo.objects.filter(Localidad__pk=localidad).values('Clave_CentroTrabajo'))).filter(Clave_Institucion__in=Subquery(DetalleCarrera.objects.filter(Clave_Carrera__areaInteres__Clave_Area=areainteres).values('Clave_Institucion'))).filter(Clave_Institucion__in = Subquery(RVOE.objects.filter(Clave_GradoAcademico__pk=nivelacademico).values('Clave_Institucion'))).filter(Dominio_Institucion=dominio))
                        InstitucionesFiltradas = serializers.serialize("json",EscuelaC.objects.filter(Localidad=localidad).filter(Dominio=dominio).filter(Nivel=nivelacademico))                    
                    else:
                        #Si no se seleccionó una localidad se filtará por municipio,Sector,Area de Interes y Nivel Academico
                        #InstitucionesFiltradas = serializers.serialize("json",Institucion.objects.filter(Clave_CentroTrabajo__in=Subquery(UbicacionCentroTrabajo.objects.filter(Localidad__in=Subquery(Localidad.objects.filter(Clave_Municipio__pk=municipio).values('Clave_Localidad'))).values('Clave_CentroTrabajo'))).filter(Clave_Institucion__in=Subquery(DetalleCarrera.objects.filter(Clave_Carrera__areaInteres__Clave_Area=areainteres).values('Clave_Institucion'))).filter(Clave_Institucion__in = Subquery(RVOE.objects.filter(Clave_GradoAcademico__pk=nivelacademico).values('Clave_Institucion'))).filter(Dominio_Institucion=dominio))
                        InstitucionesFiltradas = serializers.serialize("json",EscuelaC.objects.filter(Municipio=municipio).filter(Nivel=nivelacademico).filter(Dominio=dominio))                    

                else:
                    #Si no hay municipio seleccionado, verificamos si hay una localidad seleccionada
                    if localidad != 'empty':
                        #Si no se seleccionó municipio pero una localidad fue seleccionada de manera directa, se filtrará por la localidad seleccionada,Sector,Area de Interes y Nivel Academico
                        #InstitucionesFiltradas = serializers.serialize("json",Institucion.objects.filter(Clave_CentroTrabajo__in=Subquery(UbicacionCentroTrabajo.objects.filter(Localidad__pk=localidad).values('Clave_CentroTrabajo'))).filter(Clave_Institucion__in=Subquery(DetalleCarrera.objects.filter(Clave_Carrera__areaInteres__Clave_Area=areainteres).values('Clave_Institucion'))).filter(Clave_Institucion__in = Subquery(RVOE.objects.filter(Clave_GradoAcademico__pk=nivelacademico).values('Clave_Institucion'))).filter(Dominio_Institucion=dominio))
                        InstitucionesFiltradas = serializers.srialize("json",EscuelaC.objects.filter(Localidad=localidad).filter(Dominio=dominio).filter(Nivel=nivelacademico))
                    else:
                        #Si no se seleccionó Municipio y tampoco una localidad, se filtrarán las instituciones por Sector, Area de Interes y Nivel Academico ( SIN MUNICIPIO O LOCALIDAD)
                        #InstitucionesFiltradas = serializers.serialize("json",Institucion.objects.filter(Clave_Institucion__in=Subquery(DetalleCarrera.objects.filter(Clave_Carrera__areaInteres__Clave_Area=areainteres).values('Clave_Institucion'))).filter(Clave_Institucion__in = Subquery(RVOE.objects.filter(Clave_GradoAcademico__pk=nivelacademico).values('Clave_Institucion'))).filter(Dominio_Institucion=dominio))
                        InstitucionesFiltradas = serializers.serialize("json",EscuelaC.objects.filter(Dominio=dominio).filter(Nivel=nivelacademico))
            else:
                #Si no se seleccionó un Nivel Academico especifico, verificamos si se seleccionó algun Municipio 
                if municipio != 'empty':
                    if localidad != 'empty':
                        #Si hay una localidad seleccionada se filtará por localidad,Sector y Area de Interes (SIN NIVEL ACADEMICO)
                        #InstitucionesFiltradas = serializers.serialize("json",Institucion.objects.filter(Clave_CentroTrabajo__in=Subquery(UbicacionCentroTrabajo.objects.filter(Localidad__pk=localidad).values('Clave_CentroTrabajo'))).filter(Clave_Institucion__in=Subquery(DetalleCarrera.objects.filter(Clave_Carrera__areaInteres__Clave_Area=areainteres).values('Clave_Institucion'))).filter(Dominio_Institucion=dominio))
                        InstitucionesFiltradas = serializers.serialize("json",EscuelaC.objects.filter(Localidad=localidad).filter(Dominio=dominio))
                    else:
                        #Si no se seleccionó una localidad se filtará por municipio,Sector y Area de Interes (SIN NIVEL ACADEMICO)
                        #InstitucionesFiltradas = serializers.serialize("json",Institucion.objects.filter(Clave_CentroTrabajo__in=Subquery(UbicacionCentroTrabajo.objects.filter(Localidad__in=Subquery(Localidad.objects.filter(Clave_Municipio__pk=municipio).values('Clave_Localidad'))).values('Clave_CentroTrabajo'))).filter(Clave_Institucion__in=Subquery(DetalleCarrera.objects.filter(Clave_Carrera__areaInteres__Clave_Area=areainteres).values('Clave_Institucion'))).filter(Dominio_Institucion=dominio))
                        InstitucionesFiltradas = serializers.serialize("json",EscuelaC.objects.filter(Municipio=municipio).filter(Dominio=dominio))
                else:
                    #Si no hay Nivel Academico y tampoco hay un Municipio seleccionado, verificamos si hay una localidad seleccionada
                    if localidad != 'empty':
                        #Si no se seleccionó Nivel Academico ni municipio, pero una localidad fue seleccionada de manera directa, se filtrará por la localidad seleccionada,Sector y Area de Interes (SIN NIVEL ACADEMICO)
                        #InstitucionesFiltradas = serializers.serialize("json",Institucion.objects.filter(Clave_CentroTrabajo__in=Subquery(UbicacionCentroTrabajo.objects.filter(Localidad__pk=localidad).values('Clave_CentroTrabajo'))).filter(Clave_Institucion__in=Subquery(DetalleCarrera.objects.filter(Clave_Carrera__areaInteres__Clave_Area=areainteres).values('Clave_Institucion'))).filter(Dominio_Institucion=dominio))
                        InstitucionesFiltradas = serializers.serialize("json",EscuelaC.objects.filter(Localidad=localidad).filter(Dominio=dominio))
                    else:
                        #mod
                        #Si no se seleccionó Municipio, tampoco una localidad, ni nivel academico se filtrarán las instituciones por Sector y Area de Interes (SIN NIVEL ACADEMICO,MUNICIPIO O LOCALIDAD)
                        #InstitucionesFiltradas = serializers.serialize("json",Institucion.objects.filter(Clave_Institucion__in=Subquery(DetalleCarrera.objects.filter(Clave_Carrera__areaInteres__Clave_Area=areainteres).values('Clave_Institucion'))).filter(Dominio_Institucion=dominio))
                        InstitucionesFiltradas = serializers.serialize("json",EscuelaC.objects.filter(Dominio=dominio))
        else:
            #Si no se seleccionó ningun area de interes en particular, verificamos si se seleccionó algun Grado Academico
            if nivelacademico != 'empty':
                if municipio != 'empty':
                    if localidad != 'empty':
                        #Si hay una localidad seleccionada se filtará por localidad,Sector y Nivel Academico (SIN AREA DE INTERES)
                        #InstitucionesFiltradas = serializers.serialize("json",Institucion.objects.filter(Clave_CentroTrabajo__in=Subquery(UbicacionCentroTrabajo.objects.filter(Localidad__pk=localidad).values('Clave_CentroTrabajo'))).filter(Clave_Institucion__in = Subquery(RVOE.objects.filter(Clave_GradoAcademico__pk=nivelacademico).values('Clave_Institucion'))).filter(Dominio_Institucion=dominio))
                        InstitucionesFiltradas = serializers.serialize("json",EscuelaC.objects.filter(Localidad=localidad).filter(Dominio=dominio))
                    else:
                        #Si no se seleccionó una localidad se filtará por municipio,Sector y Nivel Academico (SIN AREA DE INTERES)
                        #InstitucionesFiltradas = serializers.serialize("json",Institucion.objects.filter(Clave_CentroTrabajo__in=Subquery(UbicacionCentroTrabajo.objects.filter(Localidad__in=Subquery(Localidad.objects.filter(Clave_Municipio__pk=municipio).values('Clave_Localidad'))).values('Clave_CentroTrabajo'))).filter(Clave_Institucion__in = Subquery(RVOE.objects.filter(Clave_GradoAcademico__pk=nivelacademico).values('Clave_Institucion'))).filter(Dominio_Institucion=dominio))
                        InstitucionesFiltradas = serializers.serialize("json",EscuelaC.objects.filter(Municipio=municipio).filter(Dominio=dominio).filter(Nivel=nivelacademico))
                else:
                    #Si no hay municipio seleccionado, verificamos si hay una localidad seleccionada
                    if localidad != 'empty':
                        #Si no se seleccionó municipio pero una localidad fue seleccionada de manera directa, se filtrará por la localidad seleccionada,Sector y Nivel Academico (SIN AREA DE INTERES)
                        #InstitucionesFiltradas = serializers.serialize("json",Institucion.objects.filter(Clave_CentroTrabajo__in=Subquery(UbicacionCentroTrabajo.objects.filter(Localidad__pk=localidad).values('Clave_CentroTrabajo'))).filter(Clave_Institucion__in = Subquery(RVOE.objects.filter(Clave_GradoAcademico__pk=nivelacademico).values('Clave_Institucion'))).filter(Dominio_Institucion=dominio))
                        InstitucionesFiltradas = serializers.serialize("json",EscuelaC.objects.filter(Localidad=localidad).filter(Dominio=dominio).filter(Nivel=nivelacademico))
                    else:
                        #Si no se seleccionó Municipio y tampoco una localidad, se filtrarán las instituciones por Sector y Nivel Academico ( SIN MUNICIPIO O LOCALIDAD NI AREA DE INTERES)
                        #InstitucionesFiltradas = serializers.serialize("json",Institucion.objects.filter(Clave_Institucion__in = Subquery(RVOE.objects.filter(Clave_GradoAcademico__pk=nivelacademico).values('Clave_Institucion'))).filter(Dominio_Institucion=dominio))
                        InstitucionesFiltradas = serializers.serialize("json",EscuelaC.objects.filter(Dominio=dominio).filter(Nivel=nivelacademico))
            else:
                #Si no se seleccionó un Nivel Academico especifico, verificamos si se seleccionó algun Municipio 
                if municipio != 'empty':
                    if localidad != 'empty':
                        #Si no hay un area de interes seleccionada y hay una localidad seleccionada se filtará por localidad y Sector(SIN NIVEL ACADEMICO , AREA DE INTERES)
                        #InstitucionesFiltradas = serializers.serialize("json",Institucion.objects.filter(Clave_CentroTrabajo__in=Subquery(UbicacionCentroTrabajo.objects.filter(Localidad__pk=localidad).values('Clave_CentroTrabajo'))).filter(Dominio_Institucion=dominio))
                        InstitucionesFiltradas = serializers.serialize("json",EscuelaC.objects.filter(Localidad=localidad).filter(Dominio=dominio))
                    else:
                        #Si no se seleccionó una localidad ni un area de interes pero si un municipio, se filtará por municipio y Sector (SIN NIVEL ACADEMICO, AREA DE INTERES)
                        #InstitucionesFiltradas = serializers.serialize("json",Institucion.objects.filter(Clave_CentroTrabajo__in=Subquery(UbicacionCentroTrabajo.objects.filter(Localidad__in=Subquery(Localidad.objects.filter(Clave_Municipio__pk=municipio).values('Clave_Localidad'))).values('Clave_CentroTrabajo'))).filter(Dominio_Institucion=dominio))
                        InstitucionesFiltradas = serializers.serialize("json",EscuelaC.objects.filter(Municipio=municipio).filter(Dominio=dominio))
                else:
                    #Si no hay Nivel Academico y tampoco hay un Municipio seleccionado, verificamos si hay una localidad seleccionada
                    if localidad != 'empty':
                        #Si no se seleccionó Nivel Academico ni municipio, pero una localidad fue seleccionada de manera directa, se filtrará por la localidad seleccionada y Sector (SIN NIVEL ACADEMICO, SIN AREA DE INTERES)
                        #InstitucionesFiltradas = serializers.serialize("json",Institucion.objects.filter(Clave_CentroTrabajo__in=Subquery(UbicacionCentroTrabajo.objects.filter(Localidad__pk=localidad).values('Clave_CentroTrabajo'))).filter(Dominio_Institucion=dominio))
                        InstitucionesFiltradas = serializers.serialize("json",EscuelaC.objects.filter(Localidad=localidad).filter(Dominio=dominio))
                    else:
                        #mod
                        #Si no se seleccionó Municipio, una localidad, nivel academico y tampoco un area de interes se filtrarán las instituciones por Sector (SIN NIVEL ACADEMICO,MUNICIPIO O LOCALIDAD,AREA DE INTERES)
                        #InstitucionesFiltradas = serializers.serialize("json",Institucion.objects.filter(Dominio_Institucion=dominio))
                        InstitucionesFiltradas = serializers.serialize("json",EscuelaC.objects.filter(Dominio=dominio))
    else:
        #Si no se seleccionó ninguna Sector/Dominio de institucion, verificamos si se eligió un Area de Interes 
        if areainteres != 'empty':
            if nivelacademico != 'empty':
                if municipio != 'empty':
                    if localidad != 'empty':
                        #Si hay una localidad seleccionada se filtará por localidad,Area de Interes y Nivel Academico (SIN SECTOR)
                        #InstitucionesFiltradas = serializers.serialize("json",Institucion.objects.filter(Clave_CentroTrabajo__in=Subquery(UbicacionCentroTrabajo.objects.filter(Localidad__pk=localidad).values('Clave_CentroTrabajo'))).filter(Clave_Institucion__in=Subquery(DetalleCarrera.objects.filter(Clave_Carrera__areaInteres__Clave_Area=areainteres).values('Clave_Institucion'))).filter(Clave_Institucion__in = Subquery(RVOE.objects.filter(Clave_GradoAcademico__pk=nivelacademico).values('Clave_Institucion'))))
                        InstitucionesFiltradas = serializers.serialize("json",EscuelaC.objects.filter(Localidad=localidad).filter(Nivel=nivelacademico))
                    else:
                        #Si no se seleccionó una localidad se filtará por municipio,Area de Interes y Nivel Academico (SIN SECTOR)
                        #InstitucionesFiltradas = serializers.serialize("json",Institucion.objects.filter(Clave_CentroTrabajo__in=Subquery(UbicacionCentroTrabajo.objects.filter(Localidad__in=Subquery(Localidad.objects.filter(Clave_Municipio__pk=municipio).values('Clave_Localidad'))).values('Clave_CentroTrabajo'))).filter(Clave_Institucion__in=Subquery(DetalleCarrera.objects.filter(Clave_Carrera__areaInteres__Clave_Area=areainteres).values('Clave_Institucion'))).filter(Clave_Institucion__in = Subquery(RVOE.objects.filter(Clave_GradoAcademico__pk=nivelacademico).values('Clave_Institucion'))))
                        InstitucionesFiltradas = serializers.serialize("json",EscuelaC.objects.filter(Municipio=municipio).filter(Nivel=nivelacademico))
                else:
                    #Si no hay municipio seleccionado, verificamos si hay una localidad seleccionada
                    if localidad != 'empty':
                        #Si no se seleccionó municipio pero una localidad fue seleccionada de manera directa, se filtrará por la localidad seleccionada,Area de Interes y Nivel Academico (SON SECTOR)
                        #InstitucionesFiltradas = serializers.serialize("json",Institucion.objects.filter(Clave_CentroTrabajo__in=Subquery(UbicacionCentroTrabajo.objects.filter(Localidad__pk=localidad).values('Clave_CentroTrabajo'))).filter(Clave_Institucion__in=Subquery(DetalleCarrera.objects.filter(Clave_Carrera__areaInteres__Clave_Area=areainteres).values('Clave_Institucion'))).filter(Clave_Institucion__in = Subquery(RVOE.objects.filter(Clave_GradoAcademico__pk=nivelacademico).values('Clave_Institucion'))))
                        InstitucionesFiltradas = serializers.serialize("json",EscuelaC.objects.filter(Localidad=localidad).filter(Nivel=nivelacademico))
                    else:
                        #Si no se seleccionó Municipio y tampoco una localidad, se filtrarán las instituciones por  Area de Interes y Nivel Academico ( SIN MUNICIPIO O LOCALIDAD, SECTOR)
                        #InstitucionesFiltradas = serializers.serialize("json",Institucion.objects.filter(Clave_Institucion__in=Subquery(DetalleCarrera.objects.filter(Clave_Carrera__areaInteres__Clave_Area=areainteres).values('Clave_Institucion'))).filter(Clave_Institucion__in = Subquery(RVOE.objects.filter(Clave_GradoAcademico__pk=nivelacademico).values('Clave_Institucion'))))
                        InstitucionesFiltradas = serializers.serialize("json",EscuelaC.objects.filter(Nivel=nivelacademico))
            else:
                #Si no se seleccionó un Nivel Academico especifico, verificamos si se seleccionó algun Municipio 
                if municipio != 'empty':
                    if localidad != 'empty':
                        #Si hay una localidad seleccionada se filtará por localidad y Area de Interes (SIN NIVEL ACADEMICO, SECTOR)
                        #InstitucionesFiltradas = serializers.serialize("json",Institucion.objects.filter(Clave_CentroTrabajo__in=Subquery(UbicacionCentroTrabajo.objects.filter(Localidad__pk=localidad).values('Clave_CentroTrabajo'))).filter(Clave_Institucion__in=Subquery(DetalleCarrera.objects.filter(Clave_Carrera__areaInteres__Clave_Area=areainteres).values('Clave_Institucion'))))
                        InstitucionesFiltradas = serializers.serialize("json",EscuelaC.objects.filter(Localidad=localidad))
                    else:
                        #Si no se seleccionó una localidad se filtará por municipio,Sector y Area de Interes (SIN NIVEL ACADEMICO,SECTOR)
                        #InstitucionesFiltradas = serializers.serialize("json",Institucion.objects.filter(Clave_CentroTrabajo__in=Subquery(UbicacionCentroTrabajo.objects.filter(Localidad__in=Subquery(Localidad.objects.filter(Clave_Municipio__pk=municipio).values('Clave_Localidad'))).values('Clave_CentroTrabajo'))).filter(Clave_Institucion__in=Subquery(DetalleCarrera.objects.filter(Clave_Carrera__areaInteres__Clave_Area=areainteres).values('Clave_Institucion'))))
                        InstitucionesFiltradas = serializers.serialize("json",EscuelaC.objects.filter(Municipio=municipio).filter(Dominio=dominio))
                else:
                    #Si no hay Nivel Academico y tampoco hay un Municipio seleccionado, verificamos si hay una localidad seleccionada
                    if localidad != 'empty':
                        #Si no se seleccionó Nivel Academico ni municipio, pero una localidad fue seleccionada de manera directa, se filtrará por la localidad seleccionada y Area de Interes (SIN NIVEL ACADEMICO,SECTOR)
                        #InstitucionesFiltradas = serializers.serialize("json",Institucion.objects.filter(Clave_CentroTrabajo__in=Subquery(UbicacionCentroTrabajo.objects.filter(Localidad__pk=localidad).values('Clave_CentroTrabajo'))).filter(Clave_Institucion__in=Subquery(DetalleCarrera.objects.filter(Clave_Carrera__areaInteres__Clave_Area=areainteres).values('Clave_Institucion'))))
                        InstitucionesFiltradas = serializers.serialize("json",EscuelaC.objects.filter(Localidad=localidad))
                    else:
                        #mod
                        #Si no se seleccionó Municipio, tampoco una localidad, ni nivel academico se filtrarán las instituciones por Sector y Area de Interes (SIN NIVEL ACADEMICO,SECTOR,MUNICIPIO O LOCALIDAD)
                        #InstitucionesFiltradas = serializers.serialize("json",Institucion.objects.filter(Clave_Institucion__in=Subquery(DetalleCarrera.objects.filter(Clave_Carrera__areaInteres__Clave_Area=areainteres).values('Clave_Institucion'))))
                        InstitucionesFiltradas = serializers.serialize("json",EscuelaC.objects.filter(Dominio=dominio))
        else:
            #Si no se seleccionó ningun area de interes en particular, verificamos si se seleccionó algun Grado Academico
            if nivelacademico != 'empty':
                if municipio != 'empty':
                    if localidad != 'empty':
                        #Si hay una localidad seleccionada se filtará por localidad,Sector y Nivel Academico (SIN AREA DE INTERES,SECTOR)
                        #InstitucionesFiltradas = serializers.serialize("json",Institucion.objects.filter(Clave_CentroTrabajo__in=Subquery(UbicacionCentroTrabajo.objects.filter(Localidad__pk=localidad).values('Clave_CentroTrabajo'))).filter(Clave_Institucion__in = Subquery(RVOE.objects.filter(Clave_GradoAcademico__pk=nivelacademico).values('Clave_Institucion'))))
                        InstitucionesFiltradas = serializers.serialize("json",EscuelaC.objects.filter(Localidad=localidad).filter(Dominio=dominio).filter(Nivel=nivelacademico))
                    else:
                        #Si no se seleccionó una localidad se filtará por municipio,Sector y Nivel Academico (SIN AREA DE INTERES,SECTOR)
                        #InstitucionesFiltradas = serializers.serialize("json",Institucion.objects.filter(Clave_CentroTrabajo__in=Subquery(UbicacionCentroTrabajo.objects.filter(Localidad__in=Subquery(Localidad.objects.filter(Clave_Municipio__pk=municipio).values('Clave_Localidad'))).values('Clave_CentroTrabajo'))).filter(Clave_Institucion__in = Subquery(RVOE.objects.filter(Clave_GradoAcademico__pk=nivelacademico).values('Clave_Institucion'))))
                        InstitucionesFiltradas = serializers.serialize("json",EscuelaC.objects.filter(Municipio=municipio).filter(Dominio=dominio).filter(Nivel=nivelacademico))
                else:
                    #Si no hay municipio seleccionado, verificamos si hay una localidad seleccionada
                    if localidad != 'empty':
                        #Si no se seleccionó municipio pero una localidad fue seleccionada de manera directa, se filtrará por la localidad seleccionada y Nivel Academico (SIN AREA DE INTERES,SECTOR)
                        #InstitucionesFiltradas = serializers.serialize("json",Institucion.objects.filter(Clave_CentroTrabajo__in=Subquery(UbicacionCentroTrabajo.objects.filter(Localidad__pk=localidad).values('Clave_CentroTrabajo'))).filter(Clave_Institucion__in = Subquery(RVOE.objects.filter(Clave_GradoAcademico__pk=nivelacademico).values('Clave_Institucion'))))
                        InstitucionesFiltradas = serializers.serialize("json",EscuelaC.objects.filter(Localidad=localidad).filter(Nivel=nivelacademico))
                    else:
                        #Si no se seleccionó Municipio y tampoco una localidad, se filtrarán las instituciones y Nivel Academico ( SIN MUNICIPIO O LOCALIDAD NI AREA DE INTERES,SECTOR)
                        #InstitucionesFiltradas = serializers.serialize("json",Institucion.objects.filter(Clave_Institucion__in = Subquery(RVOE.objects.filter(Clave_GradoAcademico__pk=nivelacademico).values('Clave_Institucion'))))
                        InstitucionesFiltradas = serializers.serialize("json",EscuelaC.objects.filter(Nivel=nivelacademico))
            else:
                #Si no se seleccionó un Nivel Academico especifico, verificamos si se seleccionó algun Municipio 
                if municipio != 'empty':
                    if localidad != 'empty':
                        #Si no hay un area de interes seleccionada y hay una localidad seleccionada se filtará por localidad y Sector(SIN NIVEL ACADEMICO , AREA DE INTERES,SECTOR)
                        #InstitucionesFiltradas = serializers.serialize("json",Institucion.objects.filter(Clave_CentroTrabajo__in=Subquery(UbicacionCentroTrabajo.objects.filter(Localidad__pk=localidad).values('Clave_CentroTrabajo'))))
                        InstitucionesFiltradas = serializers.serialize("json",EscuelaC.objects.filter(Localidad=localidad).filter(Dominio=dominio))
                    else:
                        #Si no se seleccionó una localidad ni un area de interes pero si un municipio, se filtará por municipio y Sector (SIN NIVEL ACADEMICO, AREA DE INTERES,SECTOR)
                        #InstitucionesFiltradas = serializers.serialize("json",Institucion.objects.filter(Clave_CentroTrabajo__in=Subquery(UbicacionCentroTrabajo.objects.filter(Localidad__in=Subquery(Localidad.objects.filter(Clave_Municipio__pk=municipio).values('Clave_Localidad'))).values('Clave_CentroTrabajo'))))
                        InstitucionesFiltradas = serializers.serialize("json",EscuelaC.objects.filter(Municipio=municipio))
                else:
                    #Si no hay Nivel Academico y tampoco hay un Municipio seleccionado, verificamos si hay una localidad seleccionada
                    if localidad != 'empty':
                        #Si no se seleccionó Nivel Academico ni municipio, pero una localidad fue seleccionada de manera directa, se filtrará por la localidad seleccionada (SIN NIVEL ACADEMICO, SIN AREA DE INTERES,SECTOR)
                        #InstitucionesFiltradas = serializers.serialize("json",Institucion.objects.filter(Clave_CentroTrabajo__in=Subquery(UbicacionCentroTrabajo.objects.filter(Localidad__pk=localidad).values('Clave_CentroTrabajo'))))
                        InstitucionesFiltradas = serializers.serialize("json",EscuelaC.objects.filter(Localidad=localidad))
                    else:
                        #mod
                        #Si no se seleccionó Municipio, una localidad, nivel academico y tampoco un area de interes ni un sector, las instituciones permanecerán igual.
                        #InstitucionesFiltradas = serializers.serialize("json",Institucion.objects.filter(Dominio_Institucion=dominio))
                        InstitucionesFiltradas = serializers.serialize("json",EscuelaC.objects.all())

        #InstitucionesFiltradas = serializers.serialize("json", Institucion.objects.filter(Dominio_Institucion=dominio))
    
    

    return JsonResponse(InstitucionesFiltradas,safe=False)


def instituciones(request, id, clave):
    if (id == 'id'):
            Instituciones = EscuelaC.objects.get(ClaveEscuela = clave)
            try:
                estadisticaGral = estadisticosNuevo.objects.get(ClaveEscuela=clave)
            except estadisticosNuevo.DoesNotExist:
                estadisticaGral = None

            try:
                rvoes = RVOES.objects.filter(ClaveEscuela=clave)
            except RVOES.DoesNotExist:
                rvoes = None
            
           
    else:
        Instituciones = EscuelaC.objects.get(ClaveEscuela = clave)
        try:
            estadisticaGral = estadisticosNuevo.objects.get(ClaveEscuela=clave)
        except estadisticosNuevo.DoesNotExist:
                estadisticaGral = None

        try:
            rvoes = RVOES.objects.filter(ClaveEscuela=clave)
        except RVOES.DoesNotExist:
            rvoes = None

    return render(request,'SigApp/instituciones.html',{"institucion": Instituciones,"statsg": estadisticaGral,"RVOESF":rvoes,
     })

def updInfoEstadistica(request,año,clave_ins):

    tag = 0

    if año =='primerAño':
        return JsonResponse([list(DatosEstadisticos.objects.filter(IdRVOE__in=Subquery(RVOE.objects.filter(Clave_Institucion=clave_ins).values('IdRVOE'))).aggregate(Sum('alumnosPrimerGrado')).values())[0],list(DatosEstadisticos.objects.filter(IdRVOE__in=Subquery(RVOE.objects.filter(Clave_Institucion=clave_ins).values('IdRVOE'))).aggregate(Sum('alumnosPrimerGradoHombres')).values())[0],list(DatosEstadisticos.objects.filter(IdRVOE__in=Subquery(RVOE.objects.filter(Clave_Institucion=clave_ins).values('IdRVOE'))).aggregate(Sum('alumnosPrimerGradoMujeres')).values())[0],list(DatosEstadisticos.objects.filter(IdRVOE__in=Subquery(RVOE.objects.filter(Clave_Institucion=clave_ins).values('IdRVOE'))).aggregate(Sum('alumnosIPrimerGradoHombres')).values())[0],list(DatosEstadisticos.objects.filter(IdRVOE__in=Subquery(RVOE.objects.filter(Clave_Institucion=clave_ins).values('IdRVOE'))).aggregate(Sum('alumnosIPrimerGradoMujeres')).values())[0],list(DatosEstadisticos.objects.filter(IdRVOE__in=Subquery(RVOE.objects.filter(Clave_Institucion=clave_ins).values('IdRVOE'))).aggregate(Sum('AlumnosIndigenasPrimerGrado')).values())[0]],safe=False)

    else:
        if año=='segundoAño':
            return JsonResponse([list(DatosEstadisticos.objects.filter(IdRVOE__in=Subquery(RVOE.objects.filter(Clave_Institucion=clave_ins).values('IdRVOE'))).aggregate(Sum('alumnosSegundoGrado')).values())[0],list(DatosEstadisticos.objects.filter(IdRVOE__in=Subquery(RVOE.objects.filter(Clave_Institucion=clave_ins).values('IdRVOE'))).aggregate(Sum('alumnosSegundoGradoHombres')).values())[0],list(DatosEstadisticos.objects.filter(IdRVOE__in=Subquery(RVOE.objects.filter(Clave_Institucion=clave_ins).values('IdRVOE'))).aggregate(Sum('alumnosSegundoGradoMujeres')).values())[0],list(DatosEstadisticos.objects.filter(IdRVOE__in=Subquery(RVOE.objects.filter(Clave_Institucion=clave_ins).values('IdRVOE'))).aggregate(Sum('alumnosISegundoGradoHombres')).values())[0],list(DatosEstadisticos.objects.filter(IdRVOE__in=Subquery(RVOE.objects.filter(Clave_Institucion=clave_ins).values('IdRVOE'))).aggregate(Sum('alumnosISegundoGradoMujeres')).values())[0],list(DatosEstadisticos.objects.filter(IdRVOE__in=Subquery(RVOE.objects.filter(Clave_Institucion=clave_ins).values('IdRVOE'))).aggregate(Sum('AlumnosIndigenasSegundoGrado')).values())[0]],safe=False)
            
        else:
            if año=='tercerAño':
                return JsonResponse([list(DatosEstadisticos.objects.filter(IdRVOE__in=Subquery(RVOE.objects.filter(Clave_Institucion=clave_ins).values('IdRVOE'))).aggregate(Sum('alumnosTercerGrado')).values())[0],list(DatosEstadisticos.objects.filter(IdRVOE__in=Subquery(RVOE.objects.filter(Clave_Institucion=clave_ins).values('IdRVOE'))).aggregate(Sum('alumnosTercerGradoHombres')).values())[0],list(DatosEstadisticos.objects.filter(IdRVOE__in=Subquery(RVOE.objects.filter(Clave_Institucion=clave_ins).values('IdRVOE'))).aggregate(Sum('alumnosTercerGradoMujeres')).values())[0],list(DatosEstadisticos.objects.filter(IdRVOE__in=Subquery(RVOE.objects.filter(Clave_Institucion=clave_ins).values('IdRVOE'))).aggregate(Sum('alumnosITercerGradoHombres')).values())[0],list(DatosEstadisticos.objects.filter(IdRVOE__in=Subquery(RVOE.objects.filter(Clave_Institucion=clave_ins).values('IdRVOE'))).aggregate(Sum('alumnosITercerGradoMujeres')).values())[0],list(DatosEstadisticos.objects.filter(IdRVOE__in=Subquery(RVOE.objects.filter(Clave_Institucion=clave_ins).values('IdRVOE'))).aggregate(Sum('AlumnosIndigenasTercerGrado')).values())[0]],safe=False)
                
            else:
                if año=='cuartoAño': 
                    return JsonResponse([list(DatosEstadisticos.objects.filter(IdRVOE__in=Subquery(RVOE.objects.filter(Clave_Institucion=clave_ins).values('IdRVOE'))).aggregate(Sum('alumnosCuartoGrado')).values())[0],list(DatosEstadisticos.objects.filter(IdRVOE__in=Subquery(RVOE.objects.filter(Clave_Institucion=clave_ins).values('IdRVOE'))).aggregate(Sum('alumnosCuartoGradoHombres')).values())[0],list(DatosEstadisticos.objects.filter(IdRVOE__in=Subquery(RVOE.objects.filter(Clave_Institucion=clave_ins).values('IdRVOE'))).aggregate(Sum('alumnosCuartoGradoMujeres')).values())[0],list(DatosEstadisticos.objects.filter(IdRVOE__in=Subquery(RVOE.objects.filter(Clave_Institucion=clave_ins).values('IdRVOE'))).aggregate(Sum('alumnosICuartoGradoHombres')).values())[0],list(DatosEstadisticos.objects.filter(IdRVOE__in=Subquery(RVOE.objects.filter(Clave_Institucion=clave_ins).values('IdRVOE'))).aggregate(Sum('alumnosICuartoGradoMujeres')).values())[0],list(DatosEstadisticos.objects.filter(IdRVOE__in=Subquery(RVOE.objects.filter(Clave_Institucion=clave_ins).values('IdRVOE'))).aggregate(Sum('AlumnosIndigenasCuartoGrado')).values())[0]],safe=False)
                   
                else:
                    if año=='quintoAño':
                        return JsonResponse([list(DatosEstadisticos.objects.filter(IdRVOE__in=Subquery(RVOE.objects.filter(Clave_Institucion=clave_ins).values('IdRVOE'))).aggregate(Sum('alumnosQuintoGrado')).values())[0],list(DatosEstadisticos.objects.filter(IdRVOE__in=Subquery(RVOE.objects.filter(Clave_Institucion=clave_ins).values('IdRVOE'))).aggregate(Sum('alumnosQuintoGradoHombres')).values())[0],list(DatosEstadisticos.objects.filter(IdRVOE__in=Subquery(RVOE.objects.filter(Clave_Institucion=clave_ins).values('IdRVOE'))).aggregate(Sum('alumnosQuintoGradoMujeres')).values())[0],list(DatosEstadisticos.objects.filter(IdRVOE__in=Subquery(RVOE.objects.filter(Clave_Institucion=clave_ins).values('IdRVOE'))).aggregate(Sum('alumnosIQuintoGradoHombres')).values())[0],list(DatosEstadisticos.objects.filter(IdRVOE__in=Subquery(RVOE.objects.filter(Clave_Institucion=clave_ins).values('IdRVOE'))).aggregate(Sum('alumnosIQuintoGradoMujeres')).values())[0],list(DatosEstadisticos.objects.filter(IdRVOE__in=Subquery(RVOE.objects.filter(Clave_Institucion=clave_ins).values('IdRVOE'))).aggregate(Sum('AlumnosIndigenasQuintoGrado')).values())[0]],safe=False)
                        
                    else:
                        if año=='sextoAño':
                            return JsonResponse([list(DatosEstadisticos.objects.filter(IdRVOE__in=Subquery(RVOE.objects.filter(Clave_Institucion=clave_ins).values('IdRVOE'))).aggregate(Sum('alumnosSextoGrado')).values())[0],list(DatosEstadisticos.objects.filter(IdRVOE__in=Subquery(RVOE.objects.filter(Clave_Institucion=clave_ins).values('IdRVOE'))).aggregate(Sum('alumnosSextoGradoHombres')).values())[0],list(DatosEstadisticos.objects.filter(IdRVOE__in=Subquery(RVOE.objects.filter(Clave_Institucion=clave_ins).values('IdRVOE'))).aggregate(Sum('alumnosSextoGradoMujeres')).values())[0],list(DatosEstadisticos.objects.filter(IdRVOE__in=Subquery(RVOE.objects.filter(Clave_Institucion=clave_ins).values('IdRVOE'))).aggregate(Sum('alumnosISextoGradoHombres')).values())[0],list(DatosEstadisticos.objects.filter(IdRVOE__in=Subquery(RVOE.objects.filter(Clave_Institucion=clave_ins).values('IdRVOE'))).aggregate(Sum('alumnosISextoGradoMujeres')).values())[0],list(DatosEstadisticos.objects.filter(IdRVOE__in=Subquery(RVOE.objects.filter(Clave_Institucion=clave_ins).values('IdRVOE'))).aggregate(Sum('AlumnosIndigenasSextoGrado')).values())[0]],safe=False)




    return JsonResponse(tag,safe=False)


def detalle(request,idr,inst):
    RVOEF = RVOES.objects.filter(ClaveCarrera = idr).get(ClaveEscuela=inst)
    InstitucionF = EscuelaC.objects.get(ClaveEscuela=inst)
   
    
    return render(request,'SigApp/detalle_carreras.html',{"RVOE":RVOEF,"Institucion":InstitucionF})


def miInstitucion(request,nombre):
    nombre = nombre.replace("-"," ")
    Escuela = EscuelaC.objects.get(NombreEscuela=nombre)
    modificando = False
    try:
        Temporal = DatosTemporal.objects.get(nombre_institucion=nombre)
        modificando = Temporal.modificando
    except:
        modificando = False
    
    if request.method == 'POST' and modificando == False:
        nombre2 = request.POST['nombre']
        director = request.POST['director']
        clave = request.POST['clave']
        muni = request.POST['municipio']
        loca = request.POST['localidad']
        estatus = request.POST['estatus']
        dire = request.POST['direccion']
        email = EmailMessage('Solicitud para modificar información de la institución '+ nombre,
                             'Información actual \n'
                             +'Nombre: '+nombre+'\n'
                             +'Director: '+Escuela.nombreDirector+'\n'
                             +'Clave: '+Escuela.ClaveEscuela+'\n'
                             +'Municipio: '+Escuela.Municipio+'\n'
                             +'Localidad: '+Escuela.Localidad+'\n'
                             +'Estatus: '+Escuela.EstatusEscuela+'\n'
                             +'Dirección: '+Escuela.Calle+'\n'


                             +'\nInformación a actualizar \n'
                             +'Nombre: '+ nombre2+'\n'
                             +'Director: '+director+'\n'
                             +'Clave: '+clave+'\n'
                             +'Municipio: '+muni+'\n'
                             +'Localidad: '+loca+'\n'
                             +'Estatus: '+estatus+'\n'
                             +'Dirección: '+dire+'\n',
                             to=['marcogp97@gmail.com','janeth.lopeez@gmail.com', 'ulalegriasa@ittepic.edu.mx'])
        email.send()
        nuevo = DatosTemporal(clave_centrotrabajo_temp=clave, direccion_temp = dire, director_temp=director,nombre_institucion=nombre2,municipio = muni, localidad = loca,
                            status=estatus, modificando = True)
        nuevo.save()
    elif modificando == True:
        messages.info(request, 'Ya existe una modificación en trámite, por favor espere a que sea atendida')
    if request.method == 'POST':
        form = request.FILES
        img1 = form['img1']
        Escuela.ImagenNo1=img1  
        img2 = form['img2']
        Escuela.ImagenNo2=img2
        img3 = form['img3']
        Escuela.ImagenNo3=img3
        
        Escuela.save()

    return render(request,'SigApp/miInstitucion.html',{"Escuela":Escuela})


def perfilAdmin(request):
    return render(request,'SigApp/perfilAdmin.html')

def APIapp(request, id, clave):
    if (id == 'id'):
        INF = EscuelaC.objects.filter(ClaveEscuela = clave)
        #Centro = CentroTrabajo.objects.filter(Clave_CentroTrabajo__in = Subquery(Institucion.objects.filter(Clave_Institucion=clave).values('Clave_CentroTrabajo')))
        #Ubicacion = UbicacionCentroTrabajo.objects.filter(Clave_CentroTrabajo__in = Subquery(Institucion.objects.filter(Clave_Institucion=clave).values('Clave_CentroTrabajo')))
        #NLocalidad = Localidad.objects.filter(Clave_Localidad__in = Subquery(UbicacionCentroTrabajo.objects.filter(Clave_CentroTrabajo__in=Subquery(Institucion.objects.filter(Clave_Institucion=clave).values('Clave_CentroTrabajo'))).values('Localidad')))#Clave_Localidad = Ubicacion.Localidad_id
        #NMunicipio = Municipio.objects.filter(Clave_Municipio__in=Subquery(Localidad.objects.filter(Clave_Localidad__in=Subquery(UbicacionCentroTrabajo.objects.filter(Clave_CentroTrabajo__in=Subquery(Institucion.objects.filter(Clave_Institucion=clave).values('Clave_CentroTrabajo'))).values('Localidad'))).values('Clave_Municipio')))
    else:
        INF = EscuelaC.objects.filter(ClaveEscuela = clave)
        #Centro = CentroTrabajo.objects.filter(Clave_CentroTrabajo__in = Subquery(Institucion.objects.filter(Clave_CentroTrabajo=clave).values('Clave_CentroTrabajo')))
        #Ubicacion = UbicacionCentroTrabajo.objects.filter(Clave_CentroTrabajo__in = Subquery(Institucion.objects.filter(Clave_CentroTrabajo=clave).values('Clave_CentroTrabajo')))
        #NLocalidad = Localidad.objects.filter(Clave_Localidad__in = Subquery(UbicacionCentroTrabajo.objects.filter(Clave_CentroTrabajo__in=Subquery(Institucion.objects.filter(Clave_CentroTrabajo=clave).values('Clave_CentroTrabajo'))).values('Localidad')))#Clave_Localidad = Ubicacion.Localidad_id
        #NMunicipio = Municipio.objects.filter(Clave_Municipio__in=Subquery(Localidad.objects.filter(Clave_Localidad__in=Subquery(UbicacionCentroTrabajo.objects.filter(Clave_CentroTrabajo__in=Subquery(Institucion.objects.filter(Clave_CentroTrabajo=clave).values('Clave_CentroTrabajo'))).values('Localidad'))).values('Clave_Municipio')))


    #listObjects = list(Centro) + list(INF) + list(Ubicacion) + list(NLocalidad) + list(NMunicipio)
    data =serializers.serialize("json",INF)



    return JsonResponse(data,safe=False) #,Ubicacion,NLocalidad,NMunicipio


def APIappFiltros(request, mediasuperior,superior,privada,publica):
    #SigMovilFiltros/MEDIA-SUPERIOR/empty/PRIVADO/empty/ 
    #NINGUN NIVEL, TODOS LOS SECTORES
    if publica != 'empty':publica='PÚBLICO'
    mediasuperior = mediasuperior.replace('-',' ')
    if  mediasuperior == 'empty' and superior == 'empty' and privada =='empty' and publica == 'empty':
        InstitucionesMapa = EscuelaC.objects.all()

    if  mediasuperior== 'empty' and superior =='empty' and privada =='empty' and publica != 'empty':
        InstitucionesMapa = EscuelaC.objects.filter(Dominio=publica)

    if  mediasuperior== 'empty' and superior =='empty' and privada !='empty' and publica == 'empty':
        InstitucionesMapa = EscuelaC.objects.filter(Dominio=privada)

    #NIVEL MEDIA SUPERIOR,TODOS LOS SECTORES
    if  mediasuperior != 'empty' and superior =='empty' and privada =='empty' and publica == 'empty':
        InstitucionesMapa = EscuelaC.objects.filter(Nivel=mediasuperior)
    
    if  mediasuperior != 'empty' and superior =='empty' and privada =='empty' and publica != 'empty':
        InstitucionesMapa = EscuelaC.objects.filter(Q(Nivel=mediasuperior) | Q(Dominio=publica))
    
    if  mediasuperior != 'empty' and superior =='empty' and privada !='empty' and publica == 'empty':
        InstitucionesMapa = EscuelaC.objects.filter(Q(Nivel=mediasuperior) | Q(Dominio=privada))

       #NIVEL SUPERIOR,TODOS LOS SECTORES
    if  mediasuperior == 'empty' and superior !='empty' and privada =='empty' and publica == 'empty':
        InstitucionesMapa = EscuelaC.objects.filter(Nivel=superior)
    
    if  mediasuperior == 'empty' and superior !='empty' and privada =='empty' and publica != 'empty':
        InstitucionesMapa = EscuelaC.objects.filter(Q(Nivel=superior) | Q(Dominio=publica))
    
    if  mediasuperior == 'empty' and superior !='empty' and privada !='empty' and publica == 'empty':
        InstitucionesMapa = EscuelaC.objects.filter(Q(Nivel=superior) | Q(Dominio=privada))

       #DOS NIVELES ,TODOS LOS SECTORES
    if  mediasuperior != 'empty' and superior !='empty' and privada =='empty' and publica == 'empty':
        InstitucionesMapa = EscuelaC.objects.all()

    if  mediasuperior != 'empty' and superior !='empty' and privada !='empty' and publica != 'empty':
        InstitucionesMapa = EscuelaC.objects.all()
    
    if  mediasuperior != 'empty' and superior !='empty' and privada =='empty' and publica != 'empty':
        InstitucionesMapa = EscuelaC.objects.filter(Q(Dominio=publica))
    
    if  mediasuperior != 'empty' and superior !='empty' and privada !='empty' and publica == 'empty':
        InstitucionesMapa = EscuelaC.objects.filter(Dominio=privada)
    
  
    data =serializers.serialize("json",InstitucionesMapa)



    return JsonResponse(data,safe=False) #,Ubicacion,NLocalidad,NMunicipio

def modificacionesAdmin(request):
    
    #InstitucionOri = Institucion.objects.all()
    DatosTemp = DatosTemporal.objects.all()
    return render(request,'SigApp/modificacionesAdmin.html',{
        "temporales" : DatosTemp,
    })

def mostrarInstitucion(request, nombre):
    nombre = nombre.replace("-"," ")
    #InstitucionI = Institucion.objects.get(Nombre_Institucion=nombre)
    #DireccionI = UbicacionCentroTrabajo.objects.get(Clave_CentroTrabajo=InstitucionI.Clave_CentroTrabajo.Clave_CentroTrabajo)
    Escuela = EscuelaC.objects.get(NombreEscuela=nombre)
    InstitucionT = DatosTemporal.objects.get(nombre_institucion=nombre)
    
    nombreI = nombre
    directorI = Escuela.nombreDirector
    claveI = Escuela.ClaveEscuela
    municipioI = Escuela.Municipio
    localidadI = Escuela.Localidad
    estatusI = Escuela.EstatusEscuela
    direccionI = Escuela.Calle

    nombreT = InstitucionT.nombre_institucion
    directorT = InstitucionT.director_temp
    claveT = InstitucionT.clave_centrotrabajo_temp
    municipioT = InstitucionT.municipio
    localidadT = InstitucionT.localidad
    estatusT = InstitucionT.status
    direccionT = InstitucionT.direccion_temp
 
    if request.method == 'POST':
        Escuela.NombreEscuela = nombreT
        Escuela.nombreDirector= directorT
        Escuela.ClaveEscuela = claveT
        Escuela.Municipio = municipioI
        Escuela.Localidad = localidadI
        Escuela.EstatusEscuela = estatusI
        Escuela.Calle = direccionT
        InstitucionT = False

        Escuela.save()
        DatosTemporal.objects.get(nombre_institucion = nombre).delete()
        email = EmailMessage('Se ha actualizado una institución','Información de la institución '+ Escuela.NombreEscuela+' actualizada.',to=['marcogp97@gmail.com','janeth.lopeez@gmail.com', 'ulalegriasa@ittepic.edu.mx'])
        email.send()
 
    return render(request, 'SigApp/mostrarInstitucion.html', {
       "nombreI" : nombreI, 
       "director" : directorI, 
       "clave":claveI, 
       "municipio":municipioI,
       "localidad":localidadI,
       "estatus":estatusI,
       "direccion":direccionI,
       #Temporales
       "nombreTE" : nombreT, 
       "directorTE" : directorT, 
       "claveTE":claveT, 
       "municipioTE":municipioT,
       "localidadTE":localidadT,
       "estatusTE":estatusT,
       "direccionTE":direccionT,
    })

def registrosAdmin(request):
    registro = User.objects.all()

    return render(request,'SigApp/registrosAdmin.html',{
        "registros":registro
    })

def mostrarRegistro(request, nombre):
    registroI = User.objects.get(username = nombre)
    nombreU = registroI.username
    nombreI = registroI.first_name
    emailI = registroI.email
    contrasena = registroI.password
    activo = registroI.is_active

    if request.method == 'POST':
        registroI.is_active = True
        registroI.save()
        #User.objects.get(username = nombre).delete()
        email = EmailMessage('Se ha dado de alta una institución','Registro de la institución '+ nombreU+' completado.',to=['marcogp97@gmail.com','janeth.lopeez@gmail.com', 'ulalegriasa@ittepic.edu.mx'])
        email.send()

    return render(request, 'SigApp/mostrarRegistro.html', {
        "username" : nombreU,
        "nombreI" : nombreI,
        "emailI" : emailI,
        "contrasena" : contrasena,
        "activo" : activo
    })