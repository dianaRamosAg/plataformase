from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from RVOES.models import Departamento
from login.models import CustomUser, UsuarioInstitucion
from RVOES.models import NotificacionRegistro
from .models import VisitanteSC,ConfiguracionPDF
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMessage

''' Vistas que redireccionan respecto a permisos de usuario'''
def index(request):
    return redirect('login')

def menuinstitucion(request):
    return render(request,'menuinstitucion.html')

def menuparticular(request):
    return render(request,'menuparticular.html')

def menuadmin(request):
    if request.user.tipo_usuario == '4':
        NumSolicitudes = VisitanteSC.objects.filter(leida='0').count()
        if NumSolicitudes>0:
            return render(request, 'menuadmin.html', {"numSol": NumSolicitudes})
        else:
             return render(request,'menuadmin.html')
    else:
        return redirect('perfil')

def menudepartamento(request):
    if request.user.departamento_id == '1':
        return render(request,'menudepartamento_ce.html')
    else:
        return render(request,'menudepartamento.html')

def control(request):
    return render(request,'menudepartamento_ce.html')

def menuvisitante(request):
    return render(request,'menuvisitante.html')

def cuentavisitante(request):
    return render(request,'cuentavisitante.html')

'''Función que muestra los datos de los formatos de pdf existentes.'''
def configuracionpdf(request):
    formatos = ConfiguracionPDF.objects.all()
    return render(request, 'configuracionpdf.html', {'formatos': formatos })

'''perfiluser, muestra los datos del usuario que este logueado'''
def perfiluser(request):
 
    if request.user.tipo_usuario=='1' and request.user.tipo_persona=='1':
        usrinst = UsuarioInstitucion.objects.filter(id_usuariobase=request.user.id)
        return render(request, 'perfiluserIF.html', {'usrinst': usrinst })

    else:
        if request.user.tipo_usuario=='1' and request.user.tipo_persona=='2':
            usrinst = UsuarioInstitucion.objects.filter(id_usuariobase=request.user.id)
            return render(request, 'perfiluserIM.html', {'usrinst': usrinst })
    
        if request.user.tipo_persona=='1':
            return render(request,'perfiluser.html')
        else:
            return render(request,'perfiluserMoral.html')

def visit(request):
    try:
        #Obtenemos el primer elemento de los departamentos.
        dep = Departamento.objects.get(id=1)
    except Departamento.DoesNotExist:
        #Si no existe un departamento, entonces los insertamos en la base de datos.
        a = Departamento(id=1, nombre='Control Escolar')
        a.save()
        b = Departamento(id=2, nombre='Dirección')
        b.save()
        c = Departamento(id=3, nombre='Superior')
        c.save()
        d = Departamento(id=4, nombre='Media Superior')
        d.save()
    if Departamento.objects.get(id=3)=="Superior":
         return redirect('cuentavisitante')

def notificacion(request):
    if request.method == 'POST':
        import datetime
        cad=request.POST["email"]+" ,"+request.POST["tipo_usuario"]+","+request.POST["first_name"]+" "+request.POST["last_name"]+" ,"+request.POST["celular"]+", "+request.POST["curp_rfc"]
        notificacionUsr = NotificacionRegistro(
                                        email=request.POST["email"],
                                        curp=request.POST["curp_rfc"],
                                        nombres=request.POST["first_name"]+" "+request.POST["last_name"],
                                        leida='0',
                                        celular=request.POST["celular"],
                                        tipo_usuario=request.POST["tipo_usuario"],
                                        fechaNotificacion=datetime.datetime.now(),
                                        tipo_notificacion='R',
                                        usuario_id=1)
        notificacionUsr.save()
        return render(request,'menuvisitante.html')
def notificacionadmon(request):
    """Muestra al usuario las notificaciones que tiene como no leídas.
    Parámetros
    -:param request: Contiene información del navegador del usuario que está realizando la petición.
    Retorna
    -:return: Regresa la vista en la cual el usuario podrá revisar las notificaciones que tiene que no han sido leídas.
    """
    if request.user.tipo_usuario == '4':
        import pickle # Importa una librería que nos permite la manipulación del acceso a memoria de una manera mas directa.
        NotificacionR = NotificacionRegistro.objects.filter(leida='0', tipo_notificacion='R', usuario_id=request.user.id).order_by(
            'fechaNotificacion')# Se obtienen todas las notificaciones no leídas (leida=0) de tipo 'Historial'(H) del usuario en sesión.
        s = pickle.dumps(NotificacionR)#Ponemos en memoria lo almacenado en 'Notificaciones' y almacenamos en 's' la referencia a estos datos.
        NotificacionRegistro.objects.filter(usuario_id=request.user.id, leida='0').update(leida='1')# Actualizamos las notificaciones no leídas del usuario, de "leida='0'" a "leida='1'", lo que se interpreta como que las mismas ya fueron leídas.
        NotificacionesAuxiliar = pickle.loads(s)# Almacenamos en 'NotificacionesAuxiliar' lo referenciado por 's'.
        return render(request, 'notificacionadmon.html', {"notificaciones": NotificacionesAuxiliar})
    else:
        return redirect('perfil')

#Registra al visitante como una solicitu
def regVisit(request):
    if request.method == 'POST':
        import datetime
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        curp_rfc = request.POST["curp_rfc"]
        calle = request.POST["calle"]
        password = make_password(request.POST["password"])
        noexterior = request.POST["noexterior"]
        nointerior = request.POST["nointerior"]
        codigopostal = request.POST["codigopostal"]
        municipio = request.POST["municipio"]
        colonia = request.POST["colonia"]
        celular = request.POST["celular"]
        tipo_usuario = request.POST["tipo_usuario"]
        tipo_persona = request.POST["tipo_persona"]
        # Si es tipo de usuario institución
        if tipo_usuario == '1':
            # Guardamos los datos de un centro de trabajo vinculado con la institución
            inst_cct = request.POST["cct"]
            inst_nombredirector = request.POST["nombre_director"]
            sector = request.POST["sector"]
            nivel_educativo = request.POST["nivel_educativo"]
            if nivel_educativo == 'Media Superior':
                modalidad = request.POST["modalidad"]
            else:
                modalidad = None
        else:
            inst_cct = None
            inst_nombredirector = None
            sector = None
            nivel_educativo = None
            modalidad = None
           

        visit = VisitanteSC(first_name=first_name,last_name=last_name, password=password,
                            email=email, curp_rfc=curp_rfc, calle=calle,
                            noexterior=noexterior, nointerior=nointerior, codigopostal=codigopostal,
                            municipio=municipio, colonia=colonia, celular=celular,
                            tipo_usuario=tipo_usuario,tipo_persona=tipo_persona,
                            inst_cct=inst_cct, inst_nombredirector=inst_nombredirector,
                            sector=sector, nivel_educativo=nivel_educativo,modalidad=modalidad)
        
        visit.save()
    return redirect('solicitudenviada') #mandar pagina con mensaje de esperar


def modal(request):
    return render(request,'modal.html')

#notificasiones solicitud de cuenta, muestra las nuevas solicitudes de cuenta al administrador
def notificacionsc(request):
    visitantes = VisitanteSC.objects.filter(leida='0')
    return render(request, 'notificacionsc.html', {'visitantes': visitantes })

#Funcion que manda los datos del visitante que pidió cuenta, se valida y puede aceptarse o no.
def validar(request,email):
    vs=VisitanteSC.objects.get(email = email)
    return render(request,'validar.html',{'VisitanteSC':vs})


def regUser(request, email):
    """Registra a los usuarios en la base de datos.
    Parámetros
    -:param request: Contiene información del navegador del usuario esta realizando la petición.
    -:param email: Contiene el correo de la persona que va a ser aceptada su cuenta.
    Retorna
    -:return redirect 'root': Regresa a la pantalla principal del administrador del sistema.
    -:return redirect 'signup': Regresa la vista en la cual el usuario podrá añadir nuevos usuarios.
    """
    if request.user.tipo_usuario == '4':
        usrV = VisitanteSC.objects.get(email=email)
        usr = CustomUser(username=usrV.email, email=usrV.email, password=usrV.password,
                         first_name=usrV.first_name, last_name=usrV.last_name,
                         curp_rfc=usrV.curp_rfc, calle=usrV.calle, noexterior=usrV.noexterior,
                         nointerior=usrV.nointerior, codigopostal=usrV.codigopostal,
                         municipio=usrV.municipio, colonia=usrV.colonia, celular=usrV.celular,
                         tipo_usuario=usrV.tipo_usuario, tipo_persona=usrV.tipo_persona)
        usr.save()

        #send_mail('Subject here', 'Here is the message.', 'sigssemssicyt@gmail.com', ['dianalaura.lee@gmail.com'], fail_silently=False)
        if usrV.tipo_usuario == '1':
            customUsr = CustomUser.objects.get(id=usr.id)
            usrInst = UsuarioInstitucion(id_usuariobase=customUsr, cct=usrV.inst_cct, nombredirector=usrV.inst_nombredirector,
                                         sector=usrV.sector, nivel_educativo=usrV.nivel_educativo,modalidad=usrV.modalidad)
            usrInst.save()
    VisitanteSC.objects.filter(email=usrV.email, leida='0').update(leida='1')
    email = EmailMessage('CUENTA SSEMSYCyT', 'Su cuenta ha sido aceptada, Usuario: '+usrV.email+" a partir de este momento ya puede acceder a la Plataforma de SSEMSSYCyT", to=[usrV.email])
    email.send()
    return redirect('usuarios')


         

def cancelarsolicitud(request,email2,email):
    # vs=VisitanteSC.objects.get(email = email2)
    usrV = VisitanteSC.objects.get(email=email)
    VisitanteSC.objects.filter(email=email2).delete()
    email = EmailMessage('CUENTA SSEMSYCyT', 'Su cuenta NO ha sido aceptada, Usuario: '+usrV.email+". Ante cualquier duda, comuniquese  a  SSEMSSYCyT", to=[usrV.email])
    email.send()
    return redirect('notificacionsc')

#Actualizar datos de los usuarios
def actualizarperfilusr(request):

    if request.method == 'POST':
        first_name = request.POST["first_name"]

        if request.user.tipo_persona=='1':
            last_name = request.POST["last_name"]
        else:
            last_name=""

        if request.user.tipo_usuario=='2':
            email = request.POST["email"]
            user = CustomUser.objects.get(email=email)
            if request.FILES:
                if 'firma_digital' in request.FILES:
                    user.firma_digital.delete()
                    user.firma_digital = request.FILES['firma_digital']
                     
            user.save()
        else:
            firma_digital= None

        if request.user.tipo_usuario =='1' or request.user.tipo_usuario =='5':
            identificacion = request.POST["identificacion"]
            folio_id = request.POST["folio_id"]
            marca_educativa = request.POST["marca"] 
            nombre_representante = None
            dom_legal_part = None
            if request.user.tipo_persona=='2':
                nombre_representante = request.POST["nombre_representante"] 
                dom_legal_part = request.POST["dom_legal_part"] 
                identificacion = request.POST["identificacion"]
                folio_id = request.POST["folio_id"]
                marca_educativa = request.POST["marca"] 
               

        if request.user.tipo_usuario !='1' and request.user.tipo_usuario !='5':
            identificacion = None
            folio_id = None
            marca_educativa = None
            nombre_representante = None
            dom_legal_part = None

        
        email = request.POST["email"]
        curp_rfc = request.POST["curp_rfc"]
        calle = request.POST["calle"]
        noexterior = request.POST["noexterior"]
        nointerior = request.POST["nointerior"]
        codigopostal = request.POST["codigopostal"]
        municipio = request.POST["municipio"]
        colonia = request.POST["colonia"]
        celular = request.POST["celular"]
        
        CustomUser.objects.filter(email=email).update(curp_rfc=curp_rfc,calle=calle,noexterior=noexterior,nointerior=nointerior,
        codigopostal=codigopostal,municipio=municipio,colonia=colonia,celular=celular,first_name=first_name,last_name=last_name,
        identificacion=identificacion,folio_id=folio_id,marca_educativa=marca_educativa,nombre_representante=nombre_representante,
        dom_legal_part=dom_legal_part)
   
  
    return redirect('perfiluser') 


def GuardarFormatoPDF(request):
    if request.method == 'POST':
        nombre = request.POST["nombre"]
        descripcion = request.POST["descripcion"]
        fondo = request.FILES["fondo"]
        formatoPDF= ConfiguracionPDF(nombre=nombre,descripcion=descripcion,fondo=fondo)
        formatoPDF.save()
        formatos = ConfiguracionPDF.objects.all()
        return render(request, 'configuracionpdf.html', {'formatos': formatos })
     
def cct(request):
    if request.method == 'POST':
        cct = request.POST["cct"]
        nombredirector = request.POST["nombredirector"]
        sector = request.POST["sector"]
        nivel_educativo = request.POST["nivel_educativo"]
        usr = CustomUser.objects.get(id=request.user.id)
        usrInst = UsuarioInstitucion(cct=cct, nombredirector=nombredirector, sector=sector,
                                     nivel_educativo=nivel_educativo, id_usuariobase=usr)
        usrInst.save()
    centros = UsuarioInstitucion.objects.all().order_by('cct').filter(id_usuariobase=request.user.id)
    return render(request, 'CCT.html', {'centros': centros})

def ccteditar(request,cct):
    us = UsuarioInstitucion.objects.get(cct = cct)
    return render(request,'editarcct.html',{'UsuarioInstitucion':us})

def actualizarcct(request):
    if request.method == 'POST':
        cct = request.POST["cct"]
        nombredirector = request.POST["nombredirector"]
        sector = request.POST["sector"]
        nivel_educativo = request.POST["nivel_educativo"]
        
        UsuarioInstitucion.objects.filter(cct=cct).update(nombredirector=nombredirector,sector=sector,nivel_educativo=nivel_educativo)
    return redirect('cct')
