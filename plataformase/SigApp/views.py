from django.http import HttpResponse
from django.shortcuts import render
from .models import HistorialModEstadistica, DatosTemporalEstadistica, GradoAcademico, AreaInteres, Municipio,Localidad, Institucion,CentroTrabajo,UbicacionCentroTrabajo,DetalleCarrera,Carrera,RVOE,DatosEstadisticos,Modalidad,Periodos, Escuela, DatosTemporal, EscuelaC, estadisticosNuevo,RVOES, HistorialMod
from login.models import UsuarioInstitucion
from RVOES.models import Departamento
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
from datetime import datetime

# migracion excel bd : COPY "SigApp_localidad" ("Nombre","Clave_Municipio_id") FROM 'C:\4.csv' DELIMITER ',' CSV HEADER  encoding 'windows-1251';
def index(request):
    GradosAcademicos = GradoAcademico.objects.all()
    instituciones = EscuelaC.objects.all()

    Localidades = Localidad.objects.all()

    AreasIntereses = AreaInteres.objects.all()
    Municipios = Municipio.objects.all()

    #-----------------------------------------------------------------------
    usuario = request.user.id; #OBTENER NUMERO DE INSTITUCIONES
    numInst = UsuarioInstitucion.objects.filter(id_usuariobase_id=usuario)
    nI = 0
    for i in numInst:
        nI += 1
    #-----------------------------------------------------------------------
    if request.user.is_authenticated:
        if request.user.departamento_id:

            return render(request,'SigApp/index.html',{
                "opcionesinstituciones": instituciones,

                "opcionesgrados": GradosAcademicos,
                "areaseducacion":AreasIntereses,
                "opcionesmunicipios": Municipios,
                "localidades": Localidades,
                "numeroInstituciones": nI,
                "numeroModificaciones": notificaiones(request.user.departamento_id),

            })
        else:
            return render(request,'SigApp/index.html',{
                "opcionesinstituciones": instituciones,

                "opcionesgrados": GradosAcademicos,
                "areaseducacion":AreasIntereses,
                "opcionesmunicipios": Municipios,
                "localidades": Localidades,
                "numeroInstituciones": nI,
            })
    else: 
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


def notificaiones(depart): 
    # #OBTIENE EL NUMERO DE MODIFICACIONES EN INSTITUCIÓN TANTO INFO GENERAL Y ESTADISTICA
    
    dep = Departamento.objects.get(id=depart)
    tipDep= dep.nombre.upper()
    #print(tipDep)
    #tipo de departamento usuario

    queryset = DatosTemporal.objects.all()
    
    clavesct = []
    for c in queryset:
        clavesct.append(c.clave_centrotrabajo_temp)
    #print(clavesct)
    #claves de las escuelas modfificadas 


    insList = []
    for i in clavesct:
        inst = EscuelaC.objects.get(ClaveEscuela=i)
        insList.append(inst)
    #print(insList)
    #lista completa de escuelas modificadas 

    modList = []
    for m in insList:
        if m.Nivel == "AMBOS":
            modList.append(m.ClaveEscuela)
        if m.Nivel == tipDep:
            modList.append(m.ClaveEscuela)
    #print(modList)
    #lista de escuelas solo del departamento del usuario o "AMBOS"
    
    selectMod = []
    DatosTemp = DatosTemporal.objects.all()
    nMG = 0
    for s in DatosTemp:
        for c in modList:
            if s.clave_centrotrabajo_temp == c :
                nMG += 1
                selectMod.append(s)
    #print(selectMod)
    #print(nI)
    print(nMG, "mod Granl")

    #---------- Informacion estadistica ---------------------------

    dep = Departamento.objects.get(id=depart)
    tipDep= dep.nombre.upper()
    print(tipDep)

    queryset2 = DatosTemporalEstadistica.objects.all()

    clavesct2 = []
    for c in queryset2:
        clavesct2.append(c.ClaveEscuela_temp)
    print("---1-->",clavesct2)
    #claves de las escuelas modfificadas 


    insList2 = []
    for i in clavesct2:
        inst2 = EscuelaC.objects.get(ClaveEscuela=i)
        insList2.append(inst2)
    print("---2-->",insList2)
    #lista completa de escuelas modificadas 

    modList2 = []
    for m in insList2:
        if m.Nivel == "AMBOS":
            modList2.append(m.ClaveEscuela)
        if m.Nivel == tipDep:
            modList2.append(m.ClaveEscuela)
    print("---3-->",modList2)
    #lista de claves solo del departamento del usuario o "AMBOS" 

    
    selectMod2 = []
    DatosTemp2 = DatosTemporalEstadistica.objects.all()
    nME = 0
    for s in DatosTemp2:
        for c in modList2:
            if s.ClaveEscuela_temp == c :
                nME += 1
                selectMod2.append(s)
            break
    print("---4-4-->",selectMod2)
    print(nME, "mod EStadistica")



    return nMG + nME;

def showModGral(id):

    dep = Departamento.objects.get(id=id)
    tipDep= dep.nombre.upper()
    print(tipDep)
    #tipo de departamento usuario
    #--------------------------
    queryset = DatosTemporal.objects.all()
    
    clavesct = []
    for c in queryset:
        clavesct.append(c.clave_centrotrabajo_temp)
    print(clavesct)
    #claves de las escuelas modfificadas 


    insList = []
    for i in clavesct:
        inst = EscuelaC.objects.get(ClaveEscuela=i)
        insList.append(inst)
    print(insList)
    #lista completa de escuelas modificadas 

    modList = []
    for m in insList:
        if m.Nivel == "AMBOS":
            modList.append(m.ClaveEscuela)
        if m.Nivel == tipDep:
            modList.append(m.ClaveEscuela)
    print(modList)
    #lista de escuelas solo del departamento del usuario o "AMBOS"

    selectMod = []
    DatosTemp = DatosTemporal.objects.all()
    n = 0
    for s in DatosTemp:
        for c in modList:
            if s.clave_centrotrabajo_temp == c :
                n += 1
                selectMod.append(s)
    print(selectMod)
    print(n)
    #lista de escuelas modificadas, solo del departamento del usuario 

    return selectMod;

def showModEst(id):
    #LISTA LAS MODIFICACIONES DE INF. ESTADISTICA TEMPORALES

    dep = Departamento.objects.get(id=id)
    tipDep= dep.nombre.upper()
    print(tipDep)

    queryset2 = DatosTemporalEstadistica.objects.all()

    clavesct2 = []
    for c in queryset2:
        clavesct2.append(c.ClaveEscuela_temp)
    print("---1-->",clavesct2)
    #claves de las escuelas modfificadas 


    insList2 = []
    for i in clavesct2:
        inst2 = EscuelaC.objects.get(ClaveEscuela=i)
        insList2.append(inst2)
    print("---2-->",insList2)
    #lista completa de escuelas modificadas 

    modList2 = []
    for m in insList2:
        if m.Nivel == "AMBOS":
            modList2.append(m.ClaveEscuela)
        if m.Nivel == tipDep:
            modList2.append(m.ClaveEscuela)
    print("---3-->",modList2)
    #lista de claves solo del departamento del usuario o "AMBOS" 

    
    selectMod2 = []
    DatosTemp2 = DatosTemporalEstadistica.objects.all()
    n2 = 0
    for s in DatosTemp2:
        for c in modList2:
            if s.ClaveEscuela_temp == c :
                n2 += 1
                selectMod2.append(s)
            break
    print("---4-4-->",selectMod2)
    print(n2)

    temporalesEst = []
    for c in selectMod2:
        Escuela = EscuelaC.objects.get(ClaveEscuela=c.ClaveEscuela_temp)
        temporalesEst.append({'claveEscuela': c.ClaveEscuela_temp,'nombreEscuela': Escuela.NombreEscuela, 'nombreCarrera': c.NombreCarrera_temp, 'claveCarrera': c.ClaveCarrera_temp})

    print("---5-->",temporalesEst)

    return temporalesEst;


def selecccion_municipio(request,mun):
    stackLocalidades = serializers.serialize("json",Localidad.objects.filter(Clave_Municipio__pk=mun))
    return JsonResponse(stackLocalidades,safe=False)

def localizarInst(request, clave):
     #BUSCA UNA INSTITUCION POR CLAVE Y VALIDA SI ESTA ES VALIDA
    try:
        Escuela = EscuelaC.objects.get(ClaveEscuela = clave)
    except EscuelaC.DoesNotExist:
        Escuela = None

    if Escuela != None: 
        print("--->1")
        GradosAcademicos = GradoAcademico.objects.all()
        Localidades = Localidad.objects.all()
        AreasIntereses = AreaInteres.objects.all()
        Municipios = Municipio.objects.all()
        Escuelas = EscuelaC.objects.all()
        return render(request,'SigApp/mapa_instituciones_clave.html',{
            "opcionesgrados": GradosAcademicos,
            "areaseducacion":AreasIntereses,
            "opcionesmunicipios": Municipios,
            "localidades": Localidades,
            "coordenadas": Escuelas,
            "escuela": Escuela,
        }) 
    else:
        messages.error(request, 'Clave no encontrada')
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


def localizador(request):
    #CARGA TODA LA INF. PARA LOS FILTOS DE MAPA DE INSTITUCIONES, ADEMAS DE ORDENAR TODAS LAS INSTITUCIONES
    GradosAcademicos = GradoAcademico.objects.all()
    Localidades = Localidad.objects.all()
    AreasIntereses = AreaInteres.objects.all()
    Municipios = Municipio.objects.all()
    Escuelas = EscuelaC.objects.filter(EstatusEscuela = 'ACTIVO').order_by('-Latitud') #decendente

    
    
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
        if("1" in localidad):
            localidad = localidad.replace('1','Á')
        if("2" in localidad):
            localidad = localidad.replace('2','É')
        if("3" in localidad):
            localidad = localidad.replace('3', 'Í')
        if("4" in localidad):
            localidad = localidad.replace('4', 'Ó')
        if("5" in localidad):
            localidad = localidad.replace('5', 'Ú')
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
                        InstitucionesFiltradas = serializers.serialize("json",EscuelaC.objects.filter(Municipio=municipio).filter(Localidad=localidad).filter(Dominio=dominio).filter(Nivel=nivelacademico).filter(TipoServicio = areainteres))     
                        #print('keeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')             
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
                        InstitucionesFiltradas = serializers.serialize("json",EscuelaC.objects.filter(Municipio = municipio).filter(Localidad=localidad).filter(Dominio = dominio).filter(Nivel=nivelacademico))
                        #print('pero ke a pasaooooooooooooooooooooooooooooooooooooooooo')
                    else:
                        #Si no se seleccionó una localidad se filtará por municipio,Sector y Nivel Academico (SIN AREA DE INTERES)
                        #InstitucionesFiltradas = serializers.serialize("json",Institucion.objects.filter(Clave_CentroTrabajo__in=Subquery(UbicacionCentroTrabajo.objects.filter(Localidad__in=Subquery(Localidad.objects.filter(Clave_Municipio__pk=municipio).values('Clave_Localidad'))).values('Clave_CentroTrabajo'))).filter(Clave_Institucion__in = Subquery(RVOE.objects.filter(Clave_GradoAcademico__pk=nivelacademico).values('Clave_Institucion'))).filter(Dominio_Institucion=dominio))
                        #InstitucionesFiltradas = serializers.serialize("json",EscuelaC.objects.filter(Municipio=municipio).filter(Dominio=dominio).filter(Nivel=nivelacademico))
                        InstitucionesFiltradas = serializers.serialize("json",EscuelaC.objects.filter(Municipio = municipio).filter(Dominio = dominio).filter(Nivel=nivelacademico))
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
                        InstitucionesFiltradas = serializers.serialize("json",EscuelaC.objects.filter(Municipio=municipio).filter(Nivel=nivelacademico))
                        #print('terremoto pa tu colaaaaaaaaaaaaaaaaaaaa')
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
                        InstitucionesFiltradas = serializers.serialize("json",EscuelaC.objects.filter(Municipio=municipio).filter(Localidad = localidad))
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
    
    try:
        #estadisticaGral = estadisticosNuevo.objects.get(ClaveEscuela=clave)
        Escuela = EscuelaC.objects.get(ClaveEscuela = clave)
    except EscuelaC.DoesNotExist:
        Escuela = None

    if Escuela != None:  
        if (id == 'id'):
                print("Diferente de NONE ")
                Instituciones = EscuelaC.objects.get(ClaveEscuela = clave)
                try:
                    estadisticaGral = estadisticosNuevo.objects.get(ClaveEscuela=clave)
                except estadisticosNuevo.DoesNotExist:
                    estadisticaGral = None

                try:
                    rvoes = RVOES.objects.filter(ClaveEscuela=clave)
                except RVOES.DoesNotExist:
                    rvoes = None
                
                return render(request,'SigApp/instituciones.html',{
                "institucion": Instituciones,
                "statsg": estadisticaGral,
                "RVOESF":rvoes,
            })
                
            
        else:
            print("IGUAL de NONE ")
            Instituciones = EscuelaC.objects.get(ClaveEscuela = clave)
            try:
                estadisticaGral = estadisticosNuevo.objects.get(ClaveEscuela=clave)
            except estadisticosNuevo.DoesNotExist:
                    estadisticaGral = None

            try:
                rvoes = RVOES.objects.filter(ClaveEscuela=clave)
            except RVOES.DoesNotExist:
                rvoes = None

            return render(request,'SigApp/instituciones.html',{
                "institucion": Instituciones,
                "statsg": estadisticaGral,
                "RVOESF":rvoes,
            })
    else: 
        messages.error(request, 'Clave no encontrada')
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

def institucionesUbicacion(request, id, clave):
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
        


    

def updInfoEstadistica(request,año,clave_ins): #-----#

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
   # OBTIENE INF. DEL RVOE Y DE LA INSTITUCIONES SELECCIONADA

    RVOEF = RVOES.objects.filter(ClaveCarrera = idr).get(ClaveEscuela=inst)
    InstitucionF = EscuelaC.objects.get(ClaveEscuela=inst)
   
    return render(request,'SigApp/detalle_carreras.html',{"RVOE":RVOEF,"Institucion":InstitucionF})


def selectInstitucion(request,id):
    #LISTA LOS CENTROS DE TRABAJO DE ESTE PERFIL ADEMAS NOTIFICA AL USUARIO SI UNO DE ESTOS NO SE ENCUENTRA REGISTRADO.

    queryset = UsuarioInstitucion.objects.filter(id_usuariobase_id=id) #1
    clavect = []
    for c in queryset:
        try:
            Escuela = EscuelaC.objects.get(ClaveEscuela=c.cct)
            clavect.append({'cct': c.cct,'name': Escuela.NombreEscuela, 'director': Escuela.nombreDirector})

        except EscuelaC.DoesNotExist:

            clavect.append({'cct': c.cct,'name': "Aviso! Este centro de trabajo no se encuentra registrado y no esta disponible para modificar su información", 'director': "Favor de consultar al administrador"})

    print(clavect)

    return render(request,'SigApp/selectInstitucion2.html',{
        "clavect":clavect,
        "id_dep":id,  
        })


def miInstitucion(request, id, id_dep):
    # DEVUELVE LA INF. GENERAL DE LA INSTITUCION SELECCIONADA, ADEMAS SI RECIBE UNA PETICION 
    # POST GUARDA LA INF. MODIFICADA COMO TEMPORAL Y ENVIA LA SOLICITUD PARA EL DEPARTAMENTO
    #dep = id_dep
    Escuela = EscuelaC.objects.get(ClaveEscuela=id)

    modificando = False
    try:
        Temporal = DatosTemporal.objects.get(clave_centrotrabajo_temp=id)
        modificando = Temporal.modificando
    except:
        modificando = False
    
    print(Escuela.Nivel)
    
    if request.method == 'POST' and modificando == False:
        
        nombre2 = request.POST['nombre']
        director = request.POST['director']
        clave = request.POST['clave']
        muni = request.POST['municipio']
        loca = request.POST['localidad']
        estatus = request.POST['estatus']
        dire = request.POST['direccion']
        lat = request.POST['lat']
        lng = request.POST['lng']
        usuario_mod = request.user.first_name +" "+ request.user.last_name
        email = EmailMessage('Solicitud para modificar información de la institución '+ Escuela.NombreEscuela,
                             'INFORMACIÓN ACTUAL: \n'
                             +'Nombre: '+Escuela.NombreEscuela+'\n'
                             +'Director: '+Escuela.nombreDirector+'\n'
                             +'Clave: '+Escuela.ClaveEscuela+'\n'
                             +'Municipio: '+Escuela.Municipio+'\n'
                             +'Localidad: '+Escuela.Localidad+'\n'
                             +'Estatus: '+Escuela.EstatusEscuela+'\n'
                             +'Dirección: '+Escuela.Calle+'\n'
                             
                             +'Latitud: '+Escuela.Latitud+'\n'
                             +'Longitud: '+Escuela.Longitud+'\n'
                             


                             +'\nINFORMACIÓN A ACTUALIZAR: \n'
                             +'Nombre: '+ nombre2+'\n'
                             +'Director: '+director+'\n'
                             +'Clave: '+clave+'\n'
                             +'Municipio: '+muni+'\n'
                             +'Localidad: '+loca+'\n'
                             +'Estatus: '+estatus+'\n'
                             +'Dirección: '+dire+'\n'

                             +'Latitud: '+lat+'\n'
                             +'Longitud: '+lng+'\n',
                              to=['henry.ricoe@gmail.com'])
        #email.send()
        nuevo = DatosTemporal(clave_centrotrabajo_temp=clave, direccion_temp = dire, director_temp=director,nombre_institucion=nombre2,municipio = muni, localidad = loca, status=estatus, usuario_mod=usuario_mod, latitud_temp=lat, longitud_temp=lng, modificando = True)
        nuevo.save()

        # if not request.FILES['img1']:
        #     img1 = request.FILES['img1']
        #     print(img1)
        # else:
        #     img1 = request.FILES['img1']
        #     Escuela.ImagenNo1=img1 
        #     print(img1)
        
        # if not request.FILES['img2']:
        #     img2 = request.FILES['img2']
        #     print(img2)
        # else:
        #     img2 = request.FILES['img2']
        #     Escuela.ImagenNo2=img2
        #     print(img2)

        # if not request.FILES['img3']:
        #     img3 = request.FILES['img3']
        #     print(img3)
        # else:
        #     img3 = request.FILES['img3']
        #     Escuela.ImagenNo3=img3
        #     print(img3)
    
        
        # img1 = form['img1']
        # Escuela.ImagenNo1=img1  
        # img2 = form['img2']
        # Escuela.ImagenNo2=img2
        # img3 = form['img3']
        # Escuela.ImagenNo3=img3

        if request.FILES.get('img1',False):
            img1 = request.FILES['img1']
            Escuela.ImagenNo1=img1 
            print(img1.name)
        
        if request.FILES.get('img2',False):
            img2 = request.FILES['img2']
            Escuela.ImagenNo2=img2 
            print(img2.name)

        if request.FILES.get('img3',False):
            img3 = request.FILES['img3']
            Escuela.ImagenNo3=img3 
            print(img3.name)
            
        Escuela.save()


        queryset = UsuarioInstitucion.objects.filter(id_usuariobase_id = id_dep) #1
        
        clavect = []
        for c in queryset:
            try:
                Escuela = EscuelaC.objects.get(ClaveEscuela=c.cct)
                clavect.append({'cct': c.cct,'name': Escuela.NombreEscuela, 'director': Escuela.nombreDirector})
            
            except EscuelaC.DoesNotExist:
                clavect.append({'cct': c.cct,'name': "Aviso! Este centro de trabajo no se encuentra registrado y no esta disponible para modificar su información", 'director': "Favor de consultar al administrador"})
            
        print(clavect)

        return render(request,'SigApp/selectInstitucion2.html',{
            "clavect":clavect,
            "id_dep":id_dep,  
            })
        

    elif modificando == True:
        messages.info(request, 'Ya existe una modificación en trámite, por favor espere a que sea atendida')

    
    municipios = Municipio.objects.filter()
    localidades = Localidad.objects.filter()
    

    return render(request,'SigApp/miInstitucion.html',{
        "Escuela":Escuela, 
        "modificando":modificando, 
        "municipios":municipios, 
        "localidades":localidades,
        "id_dep": id_dep,
        })


def perfilAdmin(request): # --- #
    return render(request,'SigApp/perfilAdmin.html')

def APIapp(request, id, clave):
    # API DEVULEVE TODAS LAS INSTITUCIONES.
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

def modificacionesAdmin(request, id):
    # LLAMA A LOS DEMAS METODOS PARA MOSTRAR LAS MODIFICAIONES DE INF. GENERAL,
    # MODIFICACIONES  DE INF. ESTADISTICA Y EL NUMERO DE MODIFICAIONES DE AMBAS.

    return render(request,'SigApp/modificacionesAdmin.html',{
        "temporales" : showModGral(request.user.departamento_id),
        "temporalesEst" : showModEst(request.user.departamento_id),
        "numeroModificaciones" : notificaiones(request.user.departamento_id), 
    })

def mostrarInstitucion(request, nombre):
    # OBTIENE LA INFORMACION ACTUAL Y LA TEMPORAL PARA HACER UNA COMPARATIVA 
    # SI RECIBE POST GUARDA LA NUEVA INFOMRACION, ELIMINA EL TEMPORAL, LOS REGISTRA EN EL HISTORIAL
    # *CREA Y MANDA EL EMAIL*
    # SI RECHAZA LA INF. ELIMINA EL TEMPORAL MANTIENE LA INFOMRACION ACTUAL Y REGSITRA EN HISTORIAL

    nombre = nombre.replace("-"," ")
    Escuela = EscuelaC.objects.get(NombreEscuela=nombre)
    InstitucionT = DatosTemporal.objects.get(nombre_institucion=nombre)

    idmod = InstitucionT.id
    usuario_mod = InstitucionT.usuario_mod

    claveI = Escuela.ClaveEscuela
    direccionI = Escuela.Calle
    directorI = Escuela.nombreDirector
    nombreI = nombre
    municipioI = Escuela.Municipio
    localidadI = Escuela.Localidad
    latitudI = Escuela.Latitud #
    longitudI = Escuela.Longitud #
    estatusI = Escuela.EstatusEscuela
    
    claveT = InstitucionT.clave_centrotrabajo_temp
    direccionT = InstitucionT.direccion_temp
    directorT = InstitucionT.director_temp
    nombreT = InstitucionT.nombre_institucion
    municipioT = InstitucionT.municipio
    localidadT = InstitucionT.localidad 
    latitudT = InstitucionT.latitud_temp ##
    longitudT = InstitucionT.longitud_temp ##
    estatusT = InstitucionT.status

    #dep = Departamento.objects.get(id=request.user.departamento_id)
    dep = Escuela.Nivel
    tipDep= dep.upper()
    print(tipDep)

    if request.method == 'POST':
        print("----> 2") 
        
        if request.POST.get('defaultCheck1', False):
            print("----> RECHAZADO")

            comentario = request.POST['razon']
            ''' Escuela.NombreEscuela = nombreT
            Escuela.nombreDirector= directorT
            Escuela.ClaveEscuela = claveT
            Escuela.Municipio = municipioT
            Escuela.Localidad = localidadT
            Escuela.EstatusEscuela = estatusT
            Escuela.Calle = direccionT
            Escuela.latitud = latitudT
            Escuela.longitud = longitudT '''
            InstitucionT = False
            
            #Valores de historial
            usuario_dep = request.user.first_name +" "+ request.user.last_name 
            
            clave_centrotrabajo_prev = claveI
            direccion_prev = direccionI
            director_prev = directorI
            nombre_institucion_prev = nombreI
            municipio_prev = municipioI
            localidad_prev = localidadI

            latitud_prev = latitudI ##
            longitud_prev = longitudI ##

            estatus_prev = estatusI
            #
            clave_centrotrabajo_new = claveT
            direccion_new = direccionT
            director_new = directorT
            nombre_institucion_new = nombreT
            municipio_new = municipioT
            localidad_new = localidadT

            latitud_new = latitudT ##
            longitud_new = longitudT ##

            estatus_new = estatusT
            
            nuevoHistorial = HistorialMod(fechamod = datetime.today(), 
                                        usuario_dep = usuario_dep,
                                        usuario_mod = usuario_mod,
                                        departamento = tipDep,
                                        tipo = False,
                                        comentario = comentario,
                                        clave_centrotrabajo_prev = clave_centrotrabajo_prev, 
                                        direccion_prev = direccion_prev, 
                                        director_prev=director_prev, 
                                        nombre_institucion_prev=nombre_institucion_prev, 
                                        municipio_prev = municipio_prev, 
                                        localidad_prev = localidad_prev,
                                        latitud_prev = latitud_prev, ##
                                        longitud_prev = longitud_prev, ##
                                        status_prev =estatus_prev,

                                        clave_centrotrabajo_new = clave_centrotrabajo_new, 
                                        direccion_new = direccion_new, 
                                        director_new=director_new, 
                                        nombre_institucion_new=nombre_institucion_new, 
                                        municipio_new = municipio_new, 
                                        localidad_new = localidad_new,
                                        latitud_new = latitud_new, ##
                                        longitud_new = longitud_new, ##
                                        status_new =estatus_new)
            nuevoHistorial.save()
            
            DatosTemporal.objects.get(nombre_institucion = nombre).delete()
            email = EmailMessage('<Informacion Rechaza>','La Institución: ' + Escuela.NombreEscuela + ' no ha sido actualizada. \n' 'Comentarios: ' +comentario+ ' \n',to=['henry.ricoe@gmail.com'])
            #email.send()

            #----------------------------------------------------------------

            print("Información Rechaza")
            return render(request,'SigApp/modificacionesAdmin.html',{
                "temporales" : showModGral(request.user.departamento_id),
                "temporalesEst" : showModEst(request.user.departamento_id),
                "numeroModificaciones" : notificaiones(request.user.departamento_id), 
            })
        
        else:
            print("----> ACEPTADO")
            comentario = request.POST['razon']
        
            Escuela.NombreEscuela = nombreT
            Escuela.nombreDirector= directorT
            Escuela.ClaveEscuela = claveT
            Escuela.Municipio = municipioT
            Escuela.Localidad = localidadT
            Escuela.EstatusEscuela = estatusT
            Escuela.Calle = direccionT
            Escuela.Latitud = latitudT #
            Escuela.Longitud = longitudT #
            InstitucionT = False
            
            #Valores de historial
            usuario_dep = request.user.first_name +" "+ request.user.last_name 
            
            
            clave_centrotrabajo_prev = claveI
            direccion_prev = direccionI
            director_prev = directorI
            nombre_institucion_prev = nombreI
            municipio_prev = municipioI
            localidad_prev = localidadI
            latitud_prev = latitudI ##
            longitud_prev = longitudI ##

            estatus_prev = estatusI
            #
            clave_centrotrabajo_new = claveT
            direccion_new = direccionT
            director_new = directorT
            nombre_institucion_new = nombreT
            municipio_new = municipioT
            localidad_new = localidadT
            latitud_new = latitudT ##
            longitud_new = longitudT ##
            
            estatus_new = estatusT
            
            nuevoHistorial = HistorialMod(fechamod = datetime.today(), 
                                        usuario_dep = usuario_dep,
                                        usuario_mod = usuario_mod,
                                        departamento = tipDep,
                                        tipo = True,
                                        comentario = comentario,
                                        clave_centrotrabajo_prev = clave_centrotrabajo_prev, 
                                        direccion_prev = direccion_prev, 
                                        director_prev=director_prev, 
                                        nombre_institucion_prev=nombre_institucion_prev, 
                                        municipio_prev = municipio_prev, 
                                        localidad_prev = localidad_prev,
                                        latitud_prev = latitud_prev, ##
                                        longitud_prev = longitud_prev, ##
                                        status_prev =estatus_prev,

                                        clave_centrotrabajo_new = clave_centrotrabajo_new, 
                                        direccion_new = direccion_new, 
                                        director_new=director_new, 
                                        nombre_institucion_new=nombre_institucion_new, 
                                        municipio_new = municipio_new, 
                                        localidad_new = localidad_new,
                                        latitud_new = latitud_new, ##
                                        longitud_new = longitud_new, ##
                                        status_new =estatus_new)
            nuevoHistorial.save()

            #-----------------------------------------------

            Escuela.save()
            DatosTemporal.objects.get(nombre_institucion = nombre).delete()
            email = EmailMessage('<Informacion Actualizada>','La Institución:' + Escuela.NombreEscuela + ' ha sido actualizada correctamente.',to=['henry.ricoe@gmail.com'])
            #email.send()

            #----------------------------------------------------------------
            
            return render(request,'SigApp/modificacionesAdmin.html',{
                "temporales" : showModGral(request.user.departamento_id),
                "temporalesEst" : showModEst(request.user.departamento_id),
                "numeroModificaciones" : notificaiones(request.user.departamento_id), 
            })
    
    else:
    
        print("----> 1")
            
        return render(request, 'SigApp/mostrarInstitucion.html', {
        "idmod" : idmod,
        "nombreI" : nombreI, 
        "director" : directorI, 
        "clave":claveI, 
        "municipio":municipioI,
        "localidad":localidadI,
        "latitud":latitudI, ##
        "longitud": longitudI, ##
        "estatus":estatusI,
        "direccion":direccionI,
        "nombreTE" : nombreT, 
        "directorTE" : directorT, 
        "claveTE":claveT, 
        "municipioTE":municipioT,
        "localidadTE":localidadT,
        "latitudTE": latitudT, ##
        "longitudTE": longitudT, ##
        "estatusTE":estatusT,
        "direccionTE":direccionT,
        "numeroModificaciones" : notificaiones(request.user.departamento_id), 
        })


def mostrarInstitucionEst(request, claveC, claveE):
    #OBTIENE LA INF. ESTADISTICA ACTUAL DEL RVOE, LA INF. TEMPORAL PARA COMPARAR
    # SI ES ACEPTADA GUARDA LA INFORMACION, ELIMINA EL TEMPORAL Y REGSITRA EN HISTORIAL 
    # SI ES RECHAZADA ELIMINA EL TEMPORAL REGISTRA EN HISTORIAL 

    rvoe = RVOES.objects.get(ClaveCarrera=claveC, ClaveEscuela_id=claveE)
    rvoe_temp = DatosTemporalEstadistica.objects.get(ClaveCarrera_temp=claveC, ClaveEscuela_temp=claveE)
    Escuela = EscuelaC.objects.get(ClaveEscuela=claveE)

    #dep = Departamento.objects.get(id=request.user.departamento_id)
    dep = Escuela.Nivel
    tipDep= dep.upper()
    #print(tipDep)

    if request.method == 'POST':
        print("----> 2") 
        

        if request.POST.get('defaultCheck1', False):
            print("----------------------------------------> RECHAZADO----------------------------------------")

            rvoe = RVOES.objects.get(ClaveCarrera=claveC, ClaveEscuela_id=claveE)
            rvoe_temp = DatosTemporalEstadistica.objects.get(ClaveCarrera_temp=claveC, ClaveEscuela_temp=claveE)

            comentario = request.POST['razon']
            usuario_dep = request.user.first_name +" "+ request.user.last_name 
            usuario_mod = rvoe_temp.usuario_mod
            
            #Valores de historial            
            nuevoHistorial = HistorialModEstadistica(fechamod = datetime.today(),
                                        tipo = False,
                                        comentario = comentario, 
                                        usuario_dep = usuario_dep,
                                        usuario_mod = usuario_mod,
                                        departamento = tipDep,

                                        ClaveEscuela_prev = rvoe.ClaveEscuela_id,
                                        ClaveCarrera_prev = rvoe.ClaveCarrera,
                                        NombreCarrera_prev = rvoe.NombreCarrera,

                                        TotalPrimero_prev = rvoe.TotalPrimero,
                                        TotalSegundo_prev = rvoe.TotalSegundo,
                                        TotalTercero_prev = rvoe.TotalTercero,
                                        TotalCuarto_prev = rvoe.TotalCuarto,
                                        TotalQuinto_prev = rvoe.TotalQuinto,
                                        TotalSexto_prev = rvoe.TotalSexto,
                                        TotalHombres_prev = rvoe.TotalHombres,
                                        TotalMujeres_prev = rvoe.TotalMujeres,
                                        Tipo_prev = rvoe.Tipo,
                                        Modalidad_prev = rvoe.Modalidad,
                                        Periodos_prev = rvoe.Periodos,

                                        ClaveEscuela_new= rvoe_temp.ClaveEscuela_temp,
                                        ClaveCarrera_new= rvoe_temp.ClaveCarrera_temp,
                                        NombreCarrera_new= rvoe_temp.NombreCarrera_temp,

                                        TotalPrimero_new= rvoe_temp.TotalPrimero_temp,
                                        TotalSegundo_new= rvoe_temp.TotalSegundo_temp,
                                        TotalTercero_new= rvoe_temp.TotalTercero_temp,
                                        TotalCuarto_new= rvoe_temp.TotalCuarto_temp,
                                        TotalQuinto_new= rvoe_temp.TotalQuinto_temp,
                                        TotalSexto_new= rvoe_temp.TotalSexto_temp,
                                        TotalHombres_new= rvoe_temp.TotalHombres_temp,
                                        TotalMujeres_new= rvoe_temp.TotalMujeres_temp,
                                        Tipo_new= rvoe_temp.Tipo_temp,
                                        Modalidad_new= rvoe_temp.Modalidad_temp,
                                        Periodos_new= rvoe_temp.Periodos_temp)
            nuevoHistorial.save()
            
            DatosTemporalEstadistica.objects.get(ClaveCarrera_temp=claveC, ClaveEscuela_temp=claveE).delete()
            email = EmailMessage('<Informacion Estadistica Rechaza>','La Institución: ' + Escuela.NombreEscuela + ' no ha sido actualizada. \n' 'Comentarios: ' +comentario+ ' \n',to=['henry.ricoe@gmail.com'])
            #email.send()
            rvoe.modificando = False
            rvoe.save()

            #--------------------------------------------------------------
            return render(request,'SigApp/modificacionesAdmin.html',{
                "temporales" : showModGral(request.user.departamento_id),
                "temporalesEst" : showModEst(request.user.departamento_id),
                "numeroModificaciones" : notificaiones(request.user.departamento_id), 
            })
        
        else:
            
            print("----> ACEPTADO")

            rvoe = RVOES.objects.get(ClaveCarrera=claveC, ClaveEscuela_id=claveE)
            rvoe_temp = DatosTemporalEstadistica.objects.get(ClaveCarrera_temp=claveC, ClaveEscuela_temp=claveE)

            comentario = request.POST['razon']
            usuario_dep = request.user.first_name +" "+ request.user.last_name 
            usuario_mod = rvoe_temp.usuario_mod
            
            #Actualizar datos
            rvoe.TotalPrimero = rvoe_temp.TotalPrimero_temp
            rvoe.TotalSegundo = rvoe_temp.TotalSegundo_temp
            rvoe.TotalTercero = rvoe_temp.TotalTercero_temp
            rvoe.TotalCuarto = rvoe_temp.TotalCuarto_temp
            rvoe.TotalQuinto = rvoe_temp.TotalQuinto_temp
            rvoe.TotalSexto = rvoe_temp.TotalSexto_temp
            rvoe.TotalHombres = rvoe_temp.TotalHombres_temp
            rvoe.TotalMujeres = rvoe_temp.TotalMujeres_temp
            rvoe.Tipo = rvoe_temp.Tipo_temp
            rvoe.Modalidad = rvoe_temp.Modalidad_temp
            rvoe.Periodos = rvoe_temp.Periodos_temp
            rvoe.modificando = False

            #Valores de historial
            nuevoHistorial = HistorialModEstadistica(fechamod = datetime.today(),
                                        tipo = True,
                                        comentario = comentario, 
                                        usuario_dep = usuario_dep,
                                        usuario_mod = usuario_mod,
                                        departamento = tipDep,
                                        ClaveEscuela_prev = rvoe.ClaveEscuela_id,
                                        NombreCarrera_prev = rvoe.NombreCarrera,
                                        TotalPrimero_prev = rvoe.TotalPrimero,
                                        TotalSegundo_prev = rvoe.TotalSegundo,
                                        TotalTercero_prev = rvoe.TotalTercero,
                                        TotalCuarto_prev = rvoe.TotalCuarto,
                                        TotalQuinto_prev = rvoe.TotalQuinto,
                                        TotalSexto_prev = rvoe.TotalSexto,
                                        TotalHombres_prev = rvoe.TotalHombres,
                                        TotalMujeres_prev = rvoe.TotalMujeres,
                                        Tipo_prev = rvoe.Tipo,
                                        ClaveCarrera_prev = rvoe.ClaveCarrera,
                                        Modalidad_prev = rvoe.Modalidad,
                                        Periodos_prev = rvoe.Periodos,

                                        ClaveEscuela_new = rvoe_temp.ClaveEscuela_temp,
                                        NombreCarrera_new = rvoe_temp.NombreCarrera_temp,
                                        #TotalAlumnos_new = rvoe_temp.TotalAl
                                        TotalPrimero_new = rvoe_temp.TotalPrimero_temp,
                                        TotalSegundo_new = rvoe_temp.TotalSegundo_temp,
                                        TotalTercero_new = rvoe_temp.TotalTercero_temp,
                                        TotalCuarto_new = rvoe_temp.TotalCuarto_temp,
                                        TotalQuinto_new = rvoe_temp.TotalQuinto_temp,
                                        TotalSexto_new = rvoe_temp.TotalSexto_temp,
                                        TotalHombres_new = rvoe_temp.TotalHombres_temp,
                                        TotalMujeres_new = rvoe_temp.TotalMujeres_temp,
                                        Tipo_new = rvoe_temp.Tipo_temp,
                                        ClaveCarrera_new = rvoe_temp.ClaveCarrera_temp,
                                        Modalidad_new = rvoe_temp.Modalidad_temp,
                                        Periodos_new = rvoe_temp.Periodos_temp)

            nuevoHistorial.save()
            DatosTemporalEstadistica.objects.get(ClaveCarrera_temp=claveC, ClaveEscuela_temp=claveE).delete()
            email = EmailMessage('<Informacion Estadistica Aceptada>','La Institución: ' + Escuela.NombreEscuela + ' no ha sido actualizada. \n' 'Comentarios: ' +comentario+ ' \n',to=['henry.ricoe@gmail.com'])
            
            rvoe.save()
            #email.send()

            # PRUEBAS #------------------------------------ 
            #rvoeP = RVOES.objects.get(ClaveCarrera=claveC, ClaveEscuela_id=claveE)
            #rvoeP.modificando = False
            #rvoeP.save()

            #--------------ACTUALZAR NUMEROS---------------------------------    

            total = RVOES.objects.filter(ClaveEscuela_id = claveE)
            TPri = 0
            TSeg = 0
            TTer = 0
            TCua = 0
            TQui = 0
            TSexto = 0 
            TMuj = 0 
            THom = 0

            for element in total:
                TPri += element.TotalPrimero
                TSeg += element.TotalSegundo
                TTer += element.TotalTercero
                TCua += element.TotalCuarto
                TQui += element.TotalQuinto
                TSexto += element.TotalSexto
                THom += element.TotalHombres
                TMuj += element.TotalMujeres

            totales = estadisticosNuevo.objects.get(ClaveEscuela = claveE )
            
            totales.TotalPrimero = TPri
            totales.TotalSegundo = TSeg
            totales.TotalTercero = TTer
            totales.TotalCuarto = TCua
            totales.TotalQuinto = TQui
            totales.TotalSexto = TSexto
            totales.TotalHombres = THom
            totales.TotalMujeres = TMuj
            totales.save()
            #-----------------------------------------------    
            
  
            return render(request,'SigApp/modificacionesAdmin.html',{
                "temporales" : showModGral(request.user.departamento_id),
                "temporalesEst" : showModEst(request.user.departamento_id),
                "numeroModificaciones" : notificaiones(request.user.departamento_id), 
            })
    
    else:
    
        print("----> 1")
            
        return render(request, 'SigApp/mostrarInstitucionEst.html', {
            "rvoe":rvoe,
            "rvoe_temp":rvoe_temp,
            "escuela":Escuela,
            "numeroModificaciones" : notificaiones(request.user.departamento_id), 
        })


#------------------- Historial
def listarHistorial(request):
    # OBTIENE HISTORIAL DE INF. GENERAL, TANTO DE SU DEPARTAMENTO 
    # COMO DE ALGUNO REGSITRADO CON AMBOS

    dep = Departamento.objects.get(id=request.user.departamento_id)
    tipDep= dep.nombre.upper()
    
    listaHistorial = HistorialMod.objects.filter()

    listH = []
    for m in listaHistorial:
        if m.departamento == "AMBOS":
            listH.append(m)
        if m.departamento == tipDep:
            listH.append(m)
    print(listH)

    return render(request,'SigApp/listado_historial.html',{
        "historial": listH,
        "numeroModificaciones": notificaiones(request.user.departamento_id),
    })

def listarHistorialEst(request):
    # OBTIENE HISTORIAL DE INF. ESTADISTICA, TANTO DE SU DEPARTAMENTO 
    # COMO DE ALGUNO REGSITRADO CON AMBOS

    dep = Departamento.objects.get(id=request.user.departamento_id)
    tipDep= dep.nombre.upper()
    
    listaHistorialEst = HistorialModEstadistica.objects.filter()

    listHEst = []
    for m in listaHistorialEst:
        if m.departamento == "AMBOS":
            listHEst.append(m)
        if m.departamento == tipDep:
            listHEst.append(m)
    print(listHEst)

    return render(request,'SigApp/listado_historialEst.html',{
        "historialEst": listHEst,
        "numeroModificaciones": notificaiones(request.user.departamento_id),
    })

def mostrarHistorial(request, id):
    # OBTIENE EL HISTORIAL DE INF. GENERAL REQQUERIDO 

    modificacion = HistorialMod.objects.get(id=id)
    
    return render(request,'SigApp/mostrar_historial.html',{
        "modificacion":modificacion,
        "numeroModificaciones": notificaiones(request.user.departamento_id),
    })
    
def mostrarHistorialEst(request, id):
    # OBTIENE EL HISTORIAL DE INF. ESTADISITCA REQUERIDO 

    modificacion = HistorialModEstadistica.objects.get(id=id)

    nombreEscuela = EscuelaC.objects.get(ClaveEscuela = modificacion.ClaveEscuela_new)
    print(nombreEscuela)
    
    return render(request,'SigApp/mostrar_historialEst.html',{
        "mod":modificacion,
        "escuela": nombreEscuela,
        "numeroModificaciones": notificaiones(request.user.departamento_id),
    })
#--------------------------------

def registrosAdmin(request): #----#
    registro = User.objects.all()

    return render(request,'SigApp/registrosAdmin.html',{
        "registros":registro
    })

def mostrarRegistro(request, nombre): #---#
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
        email = EmailMessage('Se ha dado de alta una institución','Registro de la institución '+ nombreU+' completado.',to=['henry.ricoe@gmail.com'])
        email.send()

    return render(request, 'SigApp/mostrarRegistro.html', {
        "username" : nombreU,
        "nombreI" : nombreI,
        "emailI" : emailI,
        "contrasena" : contrasena,
        "activo" : activo
    })

def modEstadistica(request, clave, id_dep):
    # OBTIENE EL TOTAL DE LA ESTADISTICA DE LOS RVOES, 
    # LISTA CADA UNA DE LAS CARRERAS PARA MODIFICAR 

    # if request.method == 'POST':
    #     carrera = estadisticosNuevo.objects.get(ClaveEscuela = clave)
            
    #     TotalPri = request.POST['TotalPri']
    #     TotalSeg = request.POST['TotalSeg']
    #     TotalTer = request.POST['TotalTer']
    #     TotalCua = request.POST['TotalCua']
    #     TotalQui = request.POST['TotalQui']
    #     TotalSexto = request.POST['TotalSexto']
        
    #     Totalmujeres = request.POST['TotalMujeres']
    #     Totalhombres = request.POST['TotalHombres']

    #     carrera.TotalPrimero = TotalPri
    #     carrera.TotalSegundo = TotalSeg
    #     carrera.TotalTercero = TotalTer
    #     carrera.TotalCuarto = TotalCua
    #     carrera.TotalQuinto = TotalQui
    #     carrera.TotalSexto = TotalSexto
    #     carrera.TotalMujeres = Totalmujeres
    #     carrera.TotalHombres = Totalhombres
        

    #     carrera.save()
    #     mensaje = "Actualizado Correctamente!"



    #     Escuela = EscuelaC.objects.get(ClaveEscuela = clave)

    #     try:
    #         escuelaEstadistica = estadisticosNuevo.objects.get(ClaveEscuela=clave)
    #     except estadisticosNuevo.DoesNotExist:
    #         escuelaEstadistica = None

    #     try:
    #         rvoes = RVOES.objects.filter(ClaveEscuela=clave)
    #     except RVOES.DoesNotExist:
    #         rvoes = None
        
    #     return render(request, 'SigApp/misEstadisticas.html', {
    #         'Escuela': Escuela,
    #         'infoEscuela': escuelaEstadistica,
    #         "id_dep":id_dep,  
    #         "rvoes": rvoes,
    #         "mensaje": mensaje,
    #     })
    
    
    total = RVOES.objects.filter(ClaveEscuela_id = clave)
    
    TPri = 0
    TSeg = 0
    TTer = 0
    TCua = 0
    TQui = 0
    TSexto = 0 
    TMuj = 0 
    THom = 0
    totales = []

    for element in total:
        TPri += element.TotalPrimero
        TSeg += element.TotalSegundo
        TTer += element.TotalTercero
        TCua += element.TotalCuarto
        TQui += element.TotalQuinto
        TSexto += element.TotalSexto
        THom += element.TotalHombres
        TMuj += element.TotalMujeres
    
    totales.append({'TotalPrimero': TPri,
                        'TotalSegundo': TSeg,
                        'TotalTercero': TTer,
                        'TotalCuarto': TCua,
                        'TotalQuinto': TQui,
                        'TotalSexto': TSexto,
                        'TotalHombres': THom,
                        'TotalMujeres': TMuj,
        })
    print(totales)

    
    Escuela = EscuelaC.objects.get(ClaveEscuela = clave)
    try:
        escuelaEstadistica = estadisticosNuevo.objects.get(ClaveEscuela=clave)
    except estadisticosNuevo.DoesNotExist:
        escuelaEstadistica = None
        
    if escuelaEstadistica == None:
         mensajeSinEstadistico = "Parece que aun no cuentas con estadisticas, llena los campos para darlas a conocer!"
         mensajeNuevo = "Hola! "
    else:
        mensajeSinEstadistico = "Manten tu información al día!"
        mensajeNuevo = "Hola de nuevo!"


    try:
        rvoes = RVOES.objects.filter(ClaveEscuela=clave)
    except RVOES.DoesNotExist:
        rvoes = None

    ms = False
    for element in rvoes:
        if element.Tipo == 'Bachillerato':
            ms = True
    

    sp = False
    for element in rvoes:
        if element.Tipo == 'CARRERA' or element.Tipo == 'POSGRADO':
            sp = True
    
    print(ms) 
    print(sp)

    
    return render(request, 'SigApp/misEstadisticas.html', {
        "Escuela": Escuela,
        "totales":totales,
        "infoEscuela": escuelaEstadistica,
        "id_dep": id_dep,  
        "rvoes": rvoes,
        "mensajeSinEstadistico" : mensajeSinEstadistico,
        "mensajeNuevo": mensajeNuevo,
        "msuperior": ms,
        "superior": sp,
    })



def solicitaModEstadistica(request, clave, claveE, id_dep):
# OBTIENE LA INF. ESTADISTICA PARA MOSTRAR, 
# SI RECIBE UNA PETICION POST, GUARDA LA INF. EN TEMPORAL 

    carrera = RVOES.objects.get(ClaveCarrera = clave, ClaveEscuela_id = claveE)

     
    if request.method == 'POST':
        carrera = RVOES.objects.get(ClaveCarrera = clave, ClaveEscuela_id = claveE)
            
        TotalPri = request.POST['TotalPri']
        TotalSeg = request.POST['TotalSeg']
        TotalTer = request.POST['TotalTer']
        TotalCua = request.POST['TotalCua']
        TotalQui = request.POST['TotalQui']
        TotalSexto = request.POST['TotalSexto']
        Totalmujeres = request.POST['TotalMujeres']
        Totalhombres = request.POST['TotalHombres']
        tipo = request.POST['tipo']
        periodo = request.POST['periodo']
        modalidad = request.POST['modalidad']
        usuario_mod = request.user.first_name +" "+ request.user.last_name


        temporal = DatosTemporalEstadistica(ClaveEscuela_temp = claveE,
                                             NombreCarrera_temp= carrera.NombreCarrera, 
                                             TotalPrimero_temp= TotalPri, 
                                             TotalSegundo_temp = TotalSeg, 
                                             TotalTercero_temp= TotalTer, 
                                             TotalCuarto_temp = TotalCua,
                                             TotalQuinto_temp = TotalQui,
                                             TotalSexto_temp = TotalSexto,   
                                             TotalHombres_temp= Totalhombres, 
                                             TotalMujeres_temp = Totalmujeres, 
                                             Area_temp= "",
                                             ClaveCarrera_temp = clave, 
                                             Tipo_temp= tipo, 
                                             Modalidad_temp = modalidad,
                                             Periodos_temp = periodo,
                                             usuario_mod = usuario_mod,
                                             modificando = True)
        temporal.save()

        carrera.modificando = True
        carrera.save()


        total = RVOES.objects.filter(ClaveEscuela_id = claveE)
        TPri = 0
        TSeg = 0
        TTer = 0
        TCua = 0
        TQui = 0
        TSexto = 0 
        TMuj = 0 
        THom = 0
        totales = []

        for element in total:
            TPri += element.TotalPrimero
            TSeg += element.TotalSegundo
            TTer += element.TotalTercero
            TCua += element.TotalCuarto
            TQui += element.TotalQuinto
            TSexto += element.TotalSexto
            THom += element.TotalHombres
            TMuj += element.TotalMujeres
        
        totales.append({'TotalPrimero': TPri,
                            'TotalSegundo': TSeg,
                            'TotalTercero': TTer,
                            'TotalCuarto': TCua,
                            'TotalQuinto': TQui,
                            'TotalSexto': TSexto,
                            'TotalHombres': THom,
                            'TotalMujeres': TMuj,
            })
    
        
        Escuela = EscuelaC.objects.get(ClaveEscuela = claveE)
        escuelaEstadistica = estadisticosNuevo.objects.get(ClaveEscuela=claveE)
        mensaje = "Solicitud Enviada!"

        
        try:
            escuelaEstadistica = estadisticosNuevo.objects.get(ClaveEscuela=claveE)
        except estadisticosNuevo.DoesNotExist:
            escuelaEstadistica = None
            
        if escuelaEstadistica == None:
            mensajeSinEstadistico = "Parece que aun no cuentas con estadisticas, llena los campos para darlas a conocer!"
            mensajeNuevo = "Hola por primera vez!"
        else:
            mensajeSinEstadistico = "Manten tu información al día!"
            mensajeNuevo = "Hola de nuevo!"


        try:
            rvoes = RVOES.objects.filter(ClaveEscuela=claveE)
        except RVOES.DoesNotExist:
            rvoes = None

        ms = False
        for element in rvoes:
            if element.Tipo == 'Bachillerato':
                ms = True


        sp = False
        for element in rvoes:
            if element.Tipo == 'CARRERA' or element.Tipo == 'POSGRADO':
                sp = True

        print(ms) 
        print(sp)



        #estatus de cada rvoe
        carrerastemporal = DatosTemporalEstadistica.objects.filter(ClaveCarrera_temp = clave, ClaveEscuela_temp = claveE)

        return render(request, 'SigApp/misEstadisticas.html', {
            "Escuela": Escuela,
            "infoEscuela": escuelaEstadistica,
            "totales" : totales,
            "id_dep":id_dep,  
            "rvoes": rvoes,
            "mensajeSinEstadistico" :mensajeSinEstadistico,
            "mensajeNuevo": mensajeNuevo,
            "mensaje": mensaje,
            "carrerastemporal": carrerastemporal,
            "msuperior": ms,
            "superior": sp,

        })

    Escuela = EscuelaC.objects.get(ClaveEscuela = claveE)
    escuelaEstadistica = estadisticosNuevo.objects.get(ClaveEscuela=claveE)
    

    try:
        escuelaEstadistica = estadisticosNuevo.objects.get(ClaveEscuela=claveE)
    except estadisticosNuevo.DoesNotExist:
        escuelaEstadistica = None

    try:
        rvoes = RVOES.objects.filter(ClaveEscuela=claveE)
    except RVOES.DoesNotExist:
        rvoes = None
    
    return render(request, 'SigApp/modEstadistica.html', {
        'Escuela': Escuela,
        'infoEscuela': escuelaEstadistica,
         "id_dep":id_dep,  
         "rvoes": rvoes,
         "carrera": carrera,


    })
''' 
def solicitaModeEstadistica(request, clave,claveE, id_dep):
    
    carrera = RVOES.objects.get(ClaveCarrera = clave, ClaveEscuela_id = claveE)

     
    if request.method == 'POST':
            
        TotalPri = request.POST['TotalPri']
        TotalSeg = request.POST['TotalSeg']
        TotalTer = request.POST['TotalTer']
        TotalCua = request.POST['TotalCua']
        TotalQui = request.POST['TotalQui']
        TotalSexto = request.POST['TotalSexto']
        Totalmujeres = request.POST['TotalMujeres']
        Totalhombres = request.POST['TotalHombres']
        tipo = request.POST['tipo']
        periodo = request.POST['periodo']
        modalidad = request.POST['modalidad']

        carrera.TotalPrimero = TotalPri
        carrera.TotalSegundo = TotalSeg
        carrera.TotalTercero = TotalTer
        carrera.TotalCuarto = TotalCua
        carrera.TotalQuinto = TotalQui
        carrera.TotalSexto = TotalSexto

        
        carrera.save()



        Escuela = EscuelaC.objects.get(ClaveEscuela = claveE)
        escuelaEstadistica = estadisticosNuevo.objects.get(ClaveEscuela=claveE)

        try:
            escuelaEstadistica = estadisticosNuevo.objects.get(ClaveEscuela=claveE)
        except estadisticosNuevo.DoesNotExist:
            escuelaEstadistica = None

        try:
            rvoes = RVOES.objects.filter(ClaveEscuela=claveE)
        except RVOES.DoesNotExist:
            rvoes = None
        
        return render(request, 'SigApp/misEstadisticas.html', {
            'Escuela': Escuela,
            'infoEscuela': escuelaEstadistica,
            "id_dep":id_dep,  
            "rvoes": rvoes,
            "carrera": carrera,
        })

    Escuela = EscuelaC.objects.get(ClaveEscuela = claveE)
    escuelaEstadistica = estadisticosNuevo.objects.get(ClaveEscuela=claveE)

    try:
        escuelaEstadistica = estadisticosNuevo.objects.get(ClaveEscuela=claveE)
    except estadisticosNuevo.DoesNotExist:
        escuelaEstadistica = None

    try:
        rvoes = RVOES.objects.filter(ClaveEscuela=claveE)
    except RVOES.DoesNotExist:
        rvoes = None
    
    return render(request, 'SigApp/modEstadistica.html', {
        'Escuela': Escuela,
        'infoEscuela': escuelaEstadistica,
         "id_dep":id_dep,  
         "rvoes": rvoes,
         "carrera": carrera,


    }) '''
 
    
    