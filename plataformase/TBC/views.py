from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.db.models import  Subquery
import json
from .models import * 
import sweetify
import xlwt
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from django.utils import formats
from django.core import serializers
from django.http import JsonResponse
from django.db.models import Q
#from django.utils import six 
from django.contrib.auth.hashers import make_password

# from django.apps import apps
# CustomUser  = apps.get_model('login', CustomUser)
from login.models import CustomUser, UsuarioInstitucion

import gspread
from oauth2client.service_account import ServiceAccountCredentials

global idDocente
global idAlumnoI
#idAlumnoI = 3409


'''
	Inicio de views de material didactico
'''

def catalogo_material_didactico(request,id):
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('login'))
	else:
		if request.user.tipo_usuario == '7':
			alumno_institucion = Alumno.objects.get(email=request.user.email)
			if alumno_institucion.cct != id:
				return redirect ('/TBC')
			else:
				return render(request, 'material_didactico.html')
		else:
			if request.user.tipo_usuario == '6':
				docente_institucion = Docente.objects.get(email=request.user.email)
				if docente_institucion.cct != id:
					return redirect('/TBC')
				else:
					return render(request, 'material_didactico.html')
			else:
				if request.user.tipo_usuario == '1':
					institucion = UsuarioInstitucion.objects.get(id_usuariobase=request.user.id)
					if 	institucion.cct != id:
						return redirect('/TBC')
					else:
						return render(request, 'material_didactico.html')

'''
	Fin de views de material didactico
'''

'''
Función de prueba TODO: Borrarla
'''
def resultadosTBC(request):
	return render(request,'resultadosTBC.html')

'''
Función para devolver la homePage
'''
def homePage(request):
	if not request.user.is_authenticated:
            #return render(request,'../../login/templates/registration/login.html')
			return HttpResponseRedirect(reverse('login'))
	usuarioLogueado = request.user

	#Si el usuario logeado es un docente tipo_usuario = 6, entonces se procede a asignar el idDocente correspondiente
	if usuarioLogueado.tipo_usuario == '6':
		try:
			#Para sacar el idDocente de la tabla de tbc con base en el registro CustomUser
			field_name = 'id_docente'
			obj = Docente.objects.get(email = request.user.email) #TODO: Cambiar last_name ya que se la haya dado más espacio
			field_value = getattr(obj, field_name)
			idDocente = field_value
		except:
			print('')
	
	#Si el usuario logeado es un alumno tipo_usuario = 7, entonces se procede a asignar el idAlumno correspondiente
	if usuarioLogueado.tipo_usuario == '7':
		try:
			#Para sacar el idAlumno de la tabla de tbc con base en el registro de CustomUser
			field_name = 'id_alumno'
			obj = Alumno.objects.get(email = request.user.email) #TODO:Cambiar last_name ya que se le haya dado más espacio
			field_value = getattr(obj, field_name)
			idAlumnoI = field_value
		except:
			print('')
	try:
		#Docentes = Docente.objects.get(id_docente = idDocente)
		Docentes = Docente.objects.filter(cct = usuarioLogueado.last_name)#TODO:Cambiar last_name 
		NotificacionesDocente = Notificacion_mod.objects.all()
		NotificacionesDocenteModulo = Notificacion_mod_docente.objects.filter(id_docente = idDocente)
	except:
		#Docentes = None
		NotificacionesDocente = None
		NotificacionesDocenteModulo = None
		cctDocente = None
	Cursos = Curso.objects.all()
	Alumnos = Alumno.objects.all()
	AlumnosI = Alumno.objects.filter(cct = request.user.last_name)#TODO:Cambiar last_name 
	#TODO: Sacar con el request.user.email (o sea del docente), enlazarlo con Docente y sacar su cct para hacer la consulta de abajo
	try:
		field_name = 'cct'
		obj = Docente.objects.get(email = request.user.email) #TODO:Cambiar last_name ya que se le haya dado más espacio
		field_value = getattr(obj, field_name)
		cctDocente = field_value
	except:
		print('')
	AlumnosD = Alumno.objects.filter(cct = cctDocente)
	

	if request.user.tipo_usuario == "7":
		return redirect('/TBC/actividad-alumno/'+str(idAlumnoI))

	return render(request, 'homePage.html', {'usuario':usuarioLogueado, 'notificaciones': NotificacionesDocente, 'notificacion':NotificacionesDocenteModulo, 'docente':Docentes, 'curso':Cursos, 'alumno':Alumnos, 'alumnoI':AlumnosI, 'alumnoD':AlumnosD })

'''
Función para consultar los alumnos y hacer actualización de estos
'''
def consultaAlumnos(request):
	Alumnos = Alumno.objects.all()
	Usuarios = CustomUser.objects.all()
	Archivos = Archivo.objects.all()
	if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse('login'))
	usuarioLogueado = request.user

	#Si el usuario logeado es un docente tipo_usuario = 6, entonces se procede a asignar el idDocente correspondiente
	if usuarioLogueado.tipo_usuario == '6':
		try:
			#Para sacar el idDocente de la tabla de tbc con base en el registro CustomUser
			field_name = 'id_docente'
			obj = Docente.objects.get(email = request.user.email) #TODO: Cambiar last_name ya que se la haya dado más espacio
			field_value = getattr(obj, field_name)
			idDocente = field_value
		except:
			print('')
	
	#Si el usuario logeado es un alumno tipo_usuario = 7, entonces se procede a asignar el idAlumno correspondiente
	if usuarioLogueado.tipo_usuario == '7':
		try:
			#Para sacar el idAlumno de la tabla de tbc con base en el registro de CustomUser
			field_name = 'id_alumno'
			obj = Alumno.objects.get(email = request.user.email) #TODO:Cambiar last_name ya que se le haya dado más espacio
			field_value = getattr(obj, field_name)
			idAlumnoI = field_value
		except:
			print('')

	if request.method == 'POST':
		idAlumno = request.POST['idAlumno']
		nombreAlumno = request.POST['nombreAlumno']
		email = request.POST['email']
		telFijo = request.POST['telFijo']
		telCelular = request.POST['telCelular']
		curp = request.POST['curp']
		numMatricula = request.POST['numMatricula']
		nombreEscuela = request.POST['nombreEscuela']
		cct = request.POST['cct']
		semestre = request.POST['semestre']
		contrasena = make_password(request.POST['contrasena'])
		tipo_secundaria = request.POST['tipo_secundaria']
		
		#Compara si el id está vacio para insertar nuevo reigstro
		if idAlumno == '':
			try:
				field_name = 'id_alumno'
				obj = Alumno.objects.last()
				field_value = getattr(obj, field_name)
				idAlumno = field_value + 1
			except:
				idAlumno = 1
			#try:
			nuevoAlumno = Alumno(id_alumno = idAlumno, nombre_alumno = nombreAlumno, email = email, tel_fijo = telFijo, tel_celular = telCelular, curp_alumno = curp,
			num_matricula = numMatricula, nombre_escuela = nombreEscuela, cct = cct, semestre = semestre, tipo_secundaria = tipo_secundaria)
			nuevoAlumno.save()
			nuevoAlumnoUser = CustomUser(password = contrasena, username = email, last_name = nombreAlumno, email = email, curp_rfc = curp,
			municipio = nombreEscuela, celular = telCelular, tipo_usuario = 7, tipo_persona = 1)
			#Código para guardar los archivos [acta, curp, y certificado] en la carpeta TODO: Guardar en la tabla archivo tambien
			try:
				acta = request.FILES['acta']
				#fsActa = FileSystemStorage("media/TBC/Datos/Alumnos")
				#nameActa = fsActa.save(acta.name, acta)
				#urlActa = fsActa.url(nameActa)
				#aqui guardar el registro en la tabla de archivos

				#Se obtiene el id del archivo actual para incrementar en 1 e insertarlo
				try:
					field_name = 'id_archivo'
					obj = Archivo.objects.last()
					field_value = getattr(obj, field_name)
					idArchivo = field_value + 1
				except:
					idArchivo = 1
				
				url = 'https://storage.googleapis.com/plataformase.appspot.com/TBC/archivos/registro/alumnos'+acta.name #'/media/TBC/Datos/Alumnos/'+acta.name
				nuevoArchivo = Archivo(id_archivo = idArchivo, nombre_archivo = acta.name, tipo_archivo = 'Acta nacimiento', url = url, id_alumno = idAlumno)
				nuevoArchivo.archivo = acta
				nuevoArchivo.save()
			except:
				print('')
			try:
				curp = request.FILES['curpArchivo']
				#fsCurp = FileSystemStorage("media/TBC/Datos/Alumnos")
				#nameCurp = fsCurp.save(curp.name, curp)
				#urlCurp = fsCurp.url(nameCurp)
				#aqui guardar el registro en la tabla de archivos

				try:
					field_name = 'id_archivo'
					obj = Archivo.objects.last()
					field_value = getattr(obj, field_name)
					idArchivo = field_value + 1
				except:
					idArchivo = 1
				
				url =  'https://storage.googleapis.com/plataformase.appspot.com/TBC/archivos/registro/alumnos'+curp.name #'/media/TBC/Datos/Alumnos/'+curp.name
				nuevoArchivo = Archivo(id_archivo = idArchivo, nombre_archivo = curp.name, tipo_archivo = 'Curp', url = url, id_alumno = idAlumno)
				nuevoArchivo.archivo = curp
				nuevoArchivo.save()
			except:
				print('')
			try:
				certificado = request.FILES['certificado']
				#fsCertificado = FileSystemStorage("media/TBC/Datos/Alumnos")
				#nameCertificado = fsCertificado.save(certificado.name, certificado)
				#urlCertificado = fsCertificado.url(nameCertificado)
				#aqui guardar el registro en la tabla de archivos

				try:
					field_name = 'id_archivo'
					obj = Archivo.objects.last()
					field_value = getattr(obj, field_name)
					idArchivo = field_value + 1
				except:
					idArchivo = 1
				
				url = 'https://storage.googleapis.com/plataformase.appspot.com/TBC/archivos/registro/alumnos'+certificado.name #'/media/TBC/Datos/Alumnos/'+certificado.name
				nuevoArchivo = Archivo(id_archivo = idArchivo, nombre_archivo = certificado.name, tipo_archivo = 'Certificado secundaria', url = url, id_alumno = idAlumno)
				nuevoArchivo.archivo = certificado
				nuevoArchivo.save()
			except:
				print('')
			nuevoAlumnoUser.save()
			sweetify.success(request, 'Se insertó', text='El alumno fue registrado exitosamente', persistent='Ok', icon="success")
			#except:
			#	sweetify.error(request, 'No se insertó', text='Ocurrió un error', persistent='Ok', icon="error")
		else:
			#Se pretende actualizar un registro existente
			Alumno.objects.filter(id_alumno = idAlumno).update(nombre_alumno = nombreAlumno, email = email, tel_fijo = telFijo, tel_celular = telCelular, curp_alumno = curp,
				num_matricula = numMatricula, nombre_escuela = nombreEscuela, cct = cct, semestre = semestre, tipo_secundaria = tipo_secundaria)
			#CustomUser.objects.filter(email = email).update(password = contrasena)
			sweetify.success(request, 'Se actualizó', text='El alumno fue actualizado exitosamente', persistent='Ok', icon="success")
	return render(request, 'consultaAlumnos.html', {'usuario':usuarioLogueado, "alumno":Alumnos, 'archivo':Archivos})

'''
Función para eliminar un alumnos, dado un id (id como parámetro)
'''
def delete_alumno(request, id):
	if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse('login'))
	usuarioLogueado = request.user
	AlumnoD = Alumno.objects.get(id_alumno = id)
	#AlumnoDU = CustomUser.objects.get()
	try:
		AlumnoD.delete()
		sweetify.success(request, 'Se eliminó', text='El alumno fue eliminado exitosamente', persistent='Ok', icon="success")
	except:
		sweetify.error(request, 'No se eliminó', text='Ocurrió un error', persistent='Ok', icon="error")
	return redirect('TBC:consultaAlumnos')

'''
Función para consultar el historial académico de un alumno o de un grupo
'''
def historialAcademico(request):
	Alumnos = Alumno.objects.all()
	AlumnoSel = Alumno.objects.all()
	AlumnosGrupo = None
	if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse('login'))
	usuarioLogueado = request.user

	#Si el usuario logeado es un docente tipo_usuario = 6, entonces se procede a asignar el idDocente correspondiente
	if usuarioLogueado.tipo_usuario == '6':
		try:
			#Para sacar el idDocente de la tabla de tbc con base en el registro CustomUser
			field_name = 'id_docente'
			obj = Docente.objects.get(email = request.user.email) #TODO: Cambiar last_name ya que se la haya dado más espacio
			field_value = getattr(obj, field_name)
			idDocente = field_value
		except:
			print('')
	
	#Si el usuario logeado es un alumno tipo_usuario = 7, entonces se procede a asignar el idAlumno correspondiente
	if usuarioLogueado.tipo_usuario == '7':
		try:
			#Para sacar el idAlumno de la tabla de tbc con base en el registro de CustomUser
			field_name = 'id_alumno'
			obj = Alumno.objects.get(email = request.user.email) #TODO:Cambiar last_name ya que se le haya dado más espacio
			field_value = getattr(obj, field_name)
			idAlumnoI = field_value
		except:
			print('')

	if request.method == 'POST':
		nombreAlumno = request.POST['nombreAlumno']
		try:
			AlumnoSel = Alumno.objects.get(nombre_alumno = nombreAlumno)
		except:
			grupoSel = request.POST['grupo']
			AlumnosGrupo = Alumno.objects.filter(semestre = grupoSel)
	return render(request, 'historialAcademico.html', {'usuario':usuarioLogueado, "alumno":Alumnos, "alumnoSel":AlumnoSel, 'alumnoGrupo':AlumnosGrupo }) #, "prueba":list_of_hashes})

'''
Función para realizar el pase de lista
'''
def paseLista(request):
	if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse('login'))
	usuarioLogueado = request.user

	#Si el usuario logeado es un docente tipo_usuario = 6, entonces se procede a asignar el idDocente correspondiente
	if usuarioLogueado.tipo_usuario == '6':
		try:
			#Para sacar el idDocente de la tabla de tbc con base en el registro CustomUser
			field_name = 'id_docente'
			obj = Docente.objects.get(email = request.user.email) #TODO: Cambiar last_name ya que se la haya dado más espacio
			field_value = getattr(obj, field_name)
			idDocente = field_value
		except:
			print('')
	
	#Si el usuario logeado es un alumno tipo_usuario = 7, entonces se procede a asignar el idAlumno correspondiente
	if usuarioLogueado.tipo_usuario == '7':
		try:
			#Para sacar el idAlumno de la tabla de tbc con base en el registro de CustomUser
			field_name = 'id_alumno'
			obj = Alumno.objects.get(email = request.user.email) #TODO:Cambiar last_name ya que se le haya dado más espacio
			field_value = getattr(obj, field_name)
			idAlumnoI = field_value
		except:
			print('')

	Alumnos = Alumno.objects.all()
	AlumnoSel = None
	alumnoCurso = Alumno_curso.objects.all()
	Cursos = Curso.objects.all()
	Modulos = Modulo.objects.all()
	AsistenciasG = None
	materia = None
	AlumnoSelM = None
	try:
		Docentes = Docente.objects.filter(id_docente = idDocente)
		DocenteCursos = Docente_curso.objects.filter(id_docente = idDocente)
	except:
		Docentes = None
		DocenteCursos = None

	if request.method == 'POST':
		bandera = request.POST['bandera']
		if bandera == 'False':
			try:
				#Entra para buscar un historial como docente
				print('huevos')
				materiaH = request.POST['materiaH']
				grupoH = request.POST['grupoH']
				semestreH = request.POST['semestreH']
				fechaH = ' ' + request.POST['fechaH'] + ' '
				print(grupoH, fechaH, semestreH, materiaH)
				#Aqui la materia debe ser el id_dc que cursa el alumno
				AsistenciasG = Asistencia.objects.filter(cct = grupoH, semestre = semestreH, id_dc = materiaH, fecha = fechaH)
				print('ya buscó')
			except:
				#Entra para sólo buscar algun grupo en especifico para después tomar lista
				materia = request.POST['materia']
				grupo = request.POST['grupo']
				semestre = request.POST['semestre']
				#En el template se filtra que pertenezcan a la materia
				AlumnoSel = Alumno.objects.filter(cct = grupo, semestre = semestre)
				#Se debe de sacar el id_dc de quien imparta el id_curso = materia
				field_name = 'id_dc'
				obj = Docente_curso.objects.get(id_curso = materia)
				field_value = getattr(obj, field_name)
				idDc = field_value
				AlumnoSelM = Alumno_curso.objects.filter( id_dc = idDc)
		elif bandera == 'True':
			#Entra aquí para guardar la lista
			#TODO: Jalar la lista de los campos: nombre, matricula, asistencia, retardo, justificacion
			alumnosL = request.POST.getlist('nombreAlumnoTabla') or None
			matriculasL = request.POST.getlist('matriculaAlumnoTabla') or None
			cctL = request.POST.getlist('cctL') or None
			fechaL = request.POST.getlist('fechaL') or None
			semestreL = request.POST.getlist('semestreL') or None
			id_dcL = request.POST.getlist('id_dcL') or None  
			id_alumnoL = request.POST.getlist('id_alumnoL') or None
			falta = False
			idx = 0
			#Se comprueba si ya se tomó lista ese día en ese grupo* (semestre y módulo)
			existe = Asistencia.objects.filter(fecha = fechaL[0], id_dc = id_dcL[0], cct = cctL[0], semestre = semestreL[0]).count()
			if existe > 0:
				sweetify.error(request, 'Pase de lista ya realizado', text='El pase de lista ya fue realizado previamente!', persistent='Ok', icon="info")
			else:
				for al in alumnosL:
					if not request.POST.get('Asistencia'+str(idx)):
						asistencia = False
					else:
						asistencia = True
					
					if not request.POST.get('Retardo'+str(idx)):
						retardo = False
					else:
						retardo = True
					if not request.POST.get('Justificacion'+str(idx)):
						justificacion = False
					else:
						justificacion = True
					if asistencia == False and retardo == False and justificacion == False:
						falta = True
					#Se procede a guardar los registros en la tabla de asistencia
					paseLista = Asistencia(cct = cctL[0], fecha = fechaL[0], semestre = semestreL[0], id_alumno = id_alumnoL[idx], id_dc = id_dcL[0], asistencia = asistencia, retardo = retardo, justificacion = justificacion, falta = falta)
					paseLista.save()
					#print(id_alumnoL[idx] ,al,cctL[0], fechaL[0], semestreL[0], matriculasL[idx], id_dcL[0], 'Asistencia:', asistencia, 'Retardo:', retardo, 'Justificacion:', justificacion, 'Falta:', falta)
					idx += 1
					sweetify.success(request, 'Pase de lista exitoso', text='¡El pase de lista se guardó correctamente', persistent='Ok', icon="success")

	return render(request, 'paseLista.html', {'usuario':usuarioLogueado, "alumno":Alumnos, "alumnoSel":AlumnoSel, 'docente':Docentes, 'docenteCurso':DocenteCursos, 'modulo':Modulos, 'asistencia':AsistenciasG, 'alumnoSelM':AlumnoSelM, 'alumnoCurso':alumnoCurso}) #, "prueba":list_of_hashes})


'''
Función para consultar y actualizar docentes
'''
def consultaDocentes(request):
	Docentes = Docente.objects.all()
	Archivos = Archivo.objects.all()
	if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse('login'))
	usuarioLogueado = request.user

	#Si el usuario logeado es un docente tipo_usuario = 6, entonces se procede a asignar el idDocente correspondiente
	if usuarioLogueado.tipo_usuario == '6':
		try:
			#Para sacar el idDocente de la tabla de tbc con base en el registro CustomUser
			field_name = 'id_docente'
			obj = Docente.objects.get(email = request.user.email) #TODO: Cambiar last_name ya que se la haya dado más espacio
			field_value = getattr(obj, field_name)
			idDocente = field_value
		except:
			print('')
	
	#Si el usuario logeado es un alumno tipo_usuario = 7, entonces se procede a asignar el idAlumno correspondiente
	if usuarioLogueado.tipo_usuario == '7':
		try:
			#Para sacar el idAlumno de la tabla de tbc con base en el registro de CustomUser
			field_name = 'id_alumno'
			obj = Alumno.objects.get(email = request.user.email) #TODO:Cambiar last_name ya que se le haya dado más espacio
			field_value = getattr(obj, field_name)
			idAlumnoI = field_value
		except:
			print('')

	if request.method == 'POST':
		idDocente = request.POST['idDocente']
		nombresDocente = request.POST['nombresDocente']
		apellidosDocente = request.POST['apellidosDocente']
		edad = request.POST['edad']
		email = request.POST['email']
		clave_docente = request.POST['claveDocente']
		cct = request.POST['cct']
		curp_docente = request.POST['curp']
		rfc = request.POST['rfc']
		telFijo = request.POST['telFijo']
		telCelular = request.POST['telCelular']
		nombreEscuela = request.POST['nombreEscuela']

		domicilio = request.POST['domicilio']
		num_empleado = request.POST['num_empleado']
		perfil_profesional = request.POST['perfil_profesional']
		maximo_grado = request.POST['maximo_grado']
		#curriculum = request.POST['curriculum']

		contrasena = make_password(request.POST['contrasena'])
		#Compara si el id está vacio para insertar nuevo reigstro
		if idDocente == '':
			try:
				field_name = 'id_docente'
				obj = Docente.objects.last()
				field_value = getattr(obj, field_name)
				idDocente = field_value + 1
			except:
				idDocente = 1
			try:
				nuevoDocente = Docente(id_docente = idDocente, nombres_docente = nombresDocente, apellidos_docente = apellidosDocente, edad_docente = edad, email = email, 
				clave_docente = clave_docente, cct = cct, curp_docente = curp_docente, rfc_docente = rfc, tel_fijo = telFijo, tel_cel = telCelular, nombre_escuela = nombreEscuela,
				domicilio = domicilio, num_empleado = num_empleado, perfil_profesional = perfil_profesional, maximo_grado = maximo_grado)
				nuevoDocente.save()
				nuevoDocenteU = CustomUser(password = contrasena, username = email, first_name = nombresDocente, last_name = apellidosDocente, email = email, curp_rfc = rfc, 
				municipio = nombreEscuela, tipo_usuario = 6, tipo_persona = 1)
				nuevoDocenteU.save()

				#Código para guardar los archivos [acta, curp, y certificado] en la carpeta TODO: Guardar en la tabla archivo tambien
				try:
					curriculum = request.FILES['curriculum']
					#fsCurriculum = FileSystemStorage("media/TBC/Datos/Docentes")
					#nameCurriculum = fsCurriculum.save(curriculum.name, curriculum)
					#urlCurriculum = fsCurriculum.url(nameCurriculum)
					#aqui guardar el registro en la tabla de archivos
					
					#Se obtiene el id del archivo actual para incrementar en 1 e insertarlo
					try:
						field_name = 'id_archivo'
						obj = Archivo.objects.last()
						field_value = getattr(obj, field_name)
						idArchivo = field_value + 1
					except:
						idArchivo = 1
					
					url = 'https://storage.googleapis.com/plataformase.appspot.com/TBC/archivos/registro/docentes'+curriculum.name #'/media/TBC/Datos/Docentes/'+curriculum.name
					nuevoArchivo = Archivo(id_archivo = idArchivo, nombre_archivo = curriculum.name, tipo_archivo = 'Curriculum', url = url, id_docente = idDocente)
					nuevoArchivo.archivo = curriculum
					nuevoArchivo.save()
				except:
					print('')

				sweetify.success(request, 'Se insertó', text='El docente fue registrado exitosamente', persistent='Ok', icon="success")
			except Exception as e:
				print(e)
				sweetify.error(request, 'No se insertó', text='Ocurrió un error', persistent='Ok', icon="error")
		else:
			#Se pretende actualizar un registro existente
			Docente.objects.filter(id_docente = idDocente).update(id_docente = idDocente, nombres_docente = nombresDocente, apellidos_docente = apellidosDocente, edad_docente = edad, email = email, 
				clave_docente = clave_docente, cct = cct, curp_docente = curp_docente, rfc_docente = rfc, tel_fijo = telFijo, tel_cel = telCelular, nombre_escuela = nombreEscuela,
				domicilio = domicilio, num_empleado = num_empleado, perfil_profesional = perfil_profesional, maximo_grado = maximo_grado)
			#CustomUser.objects.filter(email = email).update(password = contrasena)
			sweetify.success(request, 'Se actualizó', text='El docente fue actualizado exitosamente', persistent='Ok', icon="success")
	return render(request, 'consultaDocentes.html', {'usuario':usuarioLogueado, "docente":Docentes, 'archivo':Archivos, })

'''
Función para eliminar un docente dado su id (id como parámetro)
'''
def delete_docente(request, id):
	if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse('login'))
	usuarioLogueado = request.user
	DocentesL = Docente.objects.all()
	DocenteD = Docente.objects.get(id_docente = id)
	try:
		DocenteD.delete()
		sweetify.success(request, 'Se eliminó', text='El docente fue eliminado exitosamente', persistent='Ok', icon="success")
	except:
		sweetify.error(request, 'No se eliminó', text='El docente aun tiene cursos relacionados', persistent='Ok', icon="error")
	return redirect('TBC:consultaDocentes')

'''
Función para mostrar las actividades relacionadas al docente logeado
'''
def actividadesAprendizaje(request):
	if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse('login'))
	usuarioLogueado = request.user

	#Si el usuario logeado es un docente tipo_usuario = 6, entonces se procede a asignar el idDocente correspondiente
	if usuarioLogueado.tipo_usuario == '6':
		try:
			#Para sacar el idDocente de la tabla de tbc con base en el registro CustomUser
			field_name = 'id_docente'
			obj = Docente.objects.get(email = request.user.email) #TODO: Cambiar last_name ya que se la haya dado más espacio
			field_value = getattr(obj, field_name)
			idDocente = field_value
		except:
			print('')
	
	#Si el usuario logeado es un alumno tipo_usuario = 7, entonces se procede a asignar el idAlumno correspondiente
	if usuarioLogueado.tipo_usuario == '7':
		try:
			#Para sacar el idAlumno de la tabla de tbc con base en el registro de CustomUser
			field_name = 'id_alumno'
			obj = Alumno.objects.get(email = request.user.email) #TODO:Cambiar last_name ya que se le haya dado más espacio
			field_value = getattr(obj, field_name)
			idAlumnoI = field_value
		except:
			print('')

	Docentes = Docente.objects.filter(id_docente = idDocente)
	DocenteCursos = Docente_curso.objects.filter(id_docente = idDocente)
	Cursos = Modulo.objects.all()
	Modulos = Modulo.objects.all()
	ActividadDocente = Actividad_docente.objects.filter(id_docente = idDocente)
	NotificacionAct = Notificacion_act.objects.all()
	NotificacionActDocente = Notificacion_act_docente.objects.filter(id_docente = idDocente)
	Entregas = Entrega_actividad.objects.all()
	#Cursos = Curso.objects.filter(DocenteCurso.id_curso)

	return render(request, 'actividadesAprendizaje.html', {'usuario':usuarioLogueado, 'docente':Docentes, 'docenteCurso':DocenteCursos, 'curso':Cursos, 'modulo':Modulos,'actividad_docente': ActividadDocente, 
		'notificaciones':NotificacionAct, 'notificacion': NotificacionActDocente, 'entregas':Entregas }) 

'''
Función para insertar una actividad, datos y archivos
'''
def nuevaActividad(request):
	if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse('login'))
	usuarioLogueado = request.user

	#Si el usuario logeado es un docente tipo_usuario = 6, entonces se procede a asignar el idDocente correspondiente
	if usuarioLogueado.tipo_usuario == '6':
		try:
			#Para sacar el idDocente de la tabla de tbc con base en el registro CustomUser
			field_name = 'id_docente'
			obj = Docente.objects.get(email = request.user.email) #TODO: Cambiar last_name ya que se la haya dado más espacio
			field_value = getattr(obj, field_name)
			idDocente = field_value
		except:
			print('')
	
	c = 0
	cRub = 0
	DocenteCursos = Docente_curso.objects.filter(id_docente = idDocente)
	Cursos = Curso.objects.all()
	Modulos = Modulo.objects.all()
	
	#Si el usuario logeado es un alumno tipo_usuario = 7, entonces se procede a asignar el idAlumno correspondiente
	if usuarioLogueado.tipo_usuario == '7':
		try:
			#Para sacar el idAlumno de la tabla de tbc con base en el registro de CustomUser
			field_name = 'id_alumno'
			obj = Alumno.objects.get(email = request.user.email) #TODO:Cambiar last_name ya que se le haya dado más espacio
			field_value = getattr(obj, field_name)
			idAlumnoI = field_value
		except:
			print('')

	Docentes = Docente.objects.filter(id_docente = idDocente)
	ActividadDocente = Actividad_docente.objects.filter(id_docente = idDocente)
	if request.method == 'POST':
		nombreArchivos = ''
		nombreRubrica = ''
		try:
			field_name = 'id_actividad'
			obj = Actividad_docente.objects.last()
			field_value = getattr(obj, field_name)
			idActividad = field_value + 1
		except:
			idActividad = 1
		nombreActividad = request.POST['nombreActividad']
		unidad = request.POST['unidad']
		tipoActividad = request.POST['tipoActividad']
		tema = request.POST['tema']
		subtema = request.POST['subtema']
		objetivoActividad = request.POST['objetivoActividad']
		#Ciclo para recorrer los archivos seleccionados y guardarlos (recursos)
		for afile in request.FILES.getlist('recurso'):
			#myfile = afile
			#fs = FileSystemStorage("media/TBC/Docente/Recursos")
			#filename = fs.save(myfile.name, myfile)
			#uploaded_file_url = fs.url(filename)
			nombreArchivos += afile.name + '\n'
			#Se obtiene el id del archivo actual para incrementar en 1 e insertarlo
			try:
				field_name = 'id_archivo'
				obj = Archivo.objects.last()
				field_value = getattr(obj, field_name)
				idArchivo = field_value + 1
			except:
				idArchivo = 1
			descripcion = request.POST.getlist('descRecurso')
			url = 'https://storage.googleapis.com/plataformase.appspot.com/TBC/archivos/actividades/recursos'+afile.name #'/media/TBC/Docente/Recursos/'+afile.name
			ArchivoNuevo = Archivo(id_archivo = idArchivo, nombre_archivo = afile.name, descripcion = descripcion[c], tipo_archivo = 'Recurso', id_actividad = idActividad, url= url)
			ArchivoNuevo.archivo = afile
			ArchivoNuevo.save()
			c += 1

		#Ciclo para recorrer los archivos seleccionados y guardarlos (rubrica)
		for afile in request.FILES.getlist('rubrica'):
			#myfile = afile
			#fs = FileSystemStorage("media/TBC/Docente/Rubricas")
			#filename = fs.save(myfile.name, myfile)
			#uploaded_file_url = fs.url(filename)
			nombreRubrica += afile.name + '\n'
			#Se obtiene el id del archivo actual para incrementar en 1 e insertarlo
			try:
				field_name = 'id_archivo'
				obj = Archivo.objects.last()
				field_value = getattr(obj, field_name)
				idArchivo = field_value + 1
			except:
				idArchivo = 1
			descripcionRubrica = request.POST.getlist('descRubrica')
			url = 'https://storage.googleapis.com/plataformase.appspot.com/TBC/archivos/actividades/rubricas'+afile.name #'/media/TBC/Docente/Rubricas/'+afile.name
			ArchivoNuevo = Archivo(id_archivo = idArchivo, nombre_archivo = afile.name, descripcion = descripcionRubrica[cRub], tipo_archivo = 'Rubrica', id_actividad = idActividad, url= url)
			ArchivoNuevo.archivo = afile
			ArchivoNuevo.save()
			cRub += 1
		date_joined = datetime.now()
		formatted_datetime = formats.date_format(date_joined, "SHORT_DATETIME_FORMAT")	
		fecha = formatted_datetime
		valorActividad = request.POST['valorActividad']
		fechaHoraLimite = request.POST['fechaHoraLimite']
		modulo = request.POST['moduloActividad']
		nuevaActividad = Actividad_docente(id_actividad = idActividad, nombre_actividad = nombreActividad, unidad = unidad, tipo_actividad = tipoActividad, tema = tema,
		subtema = subtema, objetivo = objetivoActividad, valor_parcial = valorActividad, fecha_hora_limite = fechaHoraLimite,
		fechaAct = fecha, id_docente = idDocente, id_curso = modulo)
		nuevaActividad.save()
		#Se obtiene el campo id_dc de la tabla de Docente_curso
		field_name = 'id_dc'
		obj = Docente_curso.objects.get(id_docente = idDocente, id_curso = modulo)
		field_value = getattr(obj, field_name)
		idDc = field_value
		notifAct = Notificacion_act(id_dc = idDc, id_actividad = idActividad, mensaje = 'Nueva actividad', tipo = 1)
		notifAct.save()

		field_name = 'id_notificacion'
		obj = Notificacion_act.objects.last()    #.get(id_dc = idDc).last()
		field_value = getattr(obj, field_name)
		idNotif = field_value


		#TODO: Con el campo id_dc (y id_alumno resultante de consultar la tabla alumno_curso) obtener todos los id_alumno
		field_name = 'id_alumno'
		obj = Alumno_curso.objects.filter(id_dc = idDc)
		for o in obj:
			field_value = getattr(o, field_name)
			idAl = field_value
			print(idNotif)
			notifActAl = Notificacion_act_alumno(id_alumno = idAl, status = 0, id_notificacion = idNotif, id_dc = idDc)
			notifActAl.save()
		sweetify.success(request, 'Se insertó', text='La actividad fue registrado exitosamente', persistent='Ok', icon="success")
		#except:
		#	sweetify.error(request, 'No se insertó', text='Ocurrió un error', persistent='Ok', icon="error")
		return redirect('TBC:actividadesAprendizaje')

	return render(request, 'nuevaActividad.html', {'usuario':usuarioLogueado, 'docente':Docentes, 'docenteCurso':DocenteCursos, 'curso':Cursos, 'modulo':Modulos }) 

'''
Función para mostrar lo relacionado a la actividad seleccionada por su id
(id como parámetro) y para actualizar los datos de la actividad
'''
def actividadD(request, id):
	if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse('login'))
	usuarioLogueado = request.user

	#Si el usuario logeado es un docente tipo_usuario = 6, entonces se procede a asignar el idDocente correspondiente
	if usuarioLogueado.tipo_usuario == '6':
		try:
			#Para sacar el idDocente de la tabla de tbc con base en el registro CustomUser
			field_name = 'id_docente'
			obj = Docente.objects.get(email = request.user.email) #TODO: Cambiar last_name ya que se la haya dado más espacio
			field_value = getattr(obj, field_name)
			idDocente = field_value
		except:
			print('')
	
	#Si el usuario logeado es un alumno tipo_usuario = 7, entonces se procede a asignar el idAlumno correspondiente
	if usuarioLogueado.tipo_usuario == '7':
		try:
			#Para sacar el idAlumno de la tabla de tbc con base en el registro de CustomUser
			field_name = 'id_alumno'
			obj = Alumno.objects.get(email = request.user.email) #TODO:Cambiar last_name ya que se le haya dado más espacio
			field_value = getattr(obj, field_name)
			idAlumnoI = field_value
		except:
			print('')
	c = 0
	cRub = 0
	Alumnos = Alumno.objects.all()
	ActividadDocente = Actividad_docente.objects.get(id_actividad = id)
	Docentes = Docente.objects.filter(id_docente = idDocente)
	Entregas = Entrega_actividad.objects.filter(id_actividad = id)
	Archivos = Archivo.objects.filter(id_actividad = id)

	if request.method == 'POST':
		nombreArchivos = ''
		nombreRubrica = ''
		try:
			idActividad = id
			nombreActividad = request.POST['nombreActividad']
			unidad = request.POST['unidad']
			tipoActividad = request.POST['tipoActividad']
			tema = request.POST['tema']
			subtema = request.POST['subtema']
			objetivoActividad = request.POST['objetivoActividad']
			#TODO: Realizar la actualización de archivos ya subidos
			#Ciclo para recorrer los archivos seleccionados y guardarlos (recursos)
			for afile in request.FILES.getlist('recurso'):
				#myfile = afile
				#fs = FileSystemStorage("media/TBC/Docente/Recursos")
				#filename = fs.save(myfile.name, myfile)
				#uploaded_file_url = fs.url(filename)
				nombreArchivos += afile.name + '\n'
				#Se obtiene el id del archivo actual para incrementar en 1 e insertarlo
				field_name = 'id_archivo'
				obj = Archivo.objects.last()
				field_value = getattr(obj, field_name)
				idArchivo = field_value + 1
				descripcion = request.POST.getlist('descRecurso')
				url = '/TBC/archivos/'+afile.name #'/media/TBC/Docente/Recursos/'+afile.name
				ArchivoNuevo = Archivo(id_archivo = idArchivo, nombre_archivo = afile.name, descripcion = descripcion[c], tipo_archivo = 'Recurso', id_actividad = idActividad, url= url)
				ArchivoNuevo.archivo = afile
				ArchivoNuevo.save()
				c += 1

			#Ciclo para recorrer los archivos seleccionados y guardarlos (rubrica)
			for afile in request.FILES.getlist('rubrica'):
				#myfile = afile
				#fs = FileSystemStorage("media/TBC/Docente/Rubricas")
				#filename = fs.save(myfile.name, myfile)
				#uploaded_file_url = fs.url(filename)
				nombreRubrica += afile.name + '\n'
				#Se obtiene el id del archivo actual para incrementar en 1 e insertarlo
				field_name = 'id_archivo'
				obj = Archivo.objects.last()
				field_value = getattr(obj, field_name)
				idArchivo = field_value + 1
				descripcionRubrica = request.POST.getlist('descRubrica')
				url = '/TBC/archivos/'+afile.name #'/media/TBC/Docente/Rubricas/'+afile.name
				ArchivoNuevo = Archivo(id_archivo = idArchivo, nombre_archivo = afile.name, descripcion = descripcionRubrica[cRub], tipo_archivo = 'Rubrica', id_actividad = idActividad, url= url)
				ArchivoNuevo.archivo = afile
				ArchivoNuevo.save()
				cRub += 1
				
			valorActividad = request.POST['valorActividad']
			fechaHoraLimite = request.POST['fechaHoraLimite']
			Actividad_docente.objects.filter(id_actividad = id).update( nombre_actividad = nombreActividad, unidad = unidad, tipo_actividad = tipoActividad, tema = tema,
			subtema = subtema, objetivo = objetivoActividad, valor_parcial = valorActividad, fecha_hora_limite = fechaHoraLimite,
			id_docente = idDocente)
			sweetify.success(request, 'Se actualizó', text='La actividad fue actualizada exitosamente', persistent='Ok', icon="success")
		except:
			sweetify.error(request, 'No se actualizó', text='Ocurrió un error', persistent='Ok', icon="error")
		return redirect('TBC:actividadesAprendizaje')

	return render(request, 'actividadDocente.html', {'usuario':usuarioLogueado, 'actividad':ActividadDocente, 'docente':Docentes, 'alumno':Alumnos, 'entrega':Entregas , 'archivo':Archivos,}) 

'''
Función para eliminar un archivo dado su id (id como parámetro)
'''
def delete_archivo(request, idAct, tipo, name):
	if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse('login'))
	usuarioLogueado = request.user
	ArchivosL = Archivo.objects.all()
	ArchivoD = Archivo.objects.get(nombre_archivo = name)
	ArchivoD.delete()
	#TODO: Para eliminar el archivo de /media
	if tipo == 'Recurso':
		fs = FileSystemStorage("media/TBC/Docente/Recursos")
		filename = fs.delete(name)
	elif tipo == 'Rubrica':
		fs = FileSystemStorage("media/TBC/Docente/Rubricas")
		filename = fs.delete(name)

	return redirect('/TBC/actividad-docente/'+idAct)

'''
Función para eliminar una actividad dada su id (id como parámetro)
'''
def delete_actividad(request, id):
	if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse('login'))
	usuarioLogueado = request.user
	ActividadDocenteD = Actividad_docente.objects.get(id_actividad = id)
	Notificacion_actD = Notificacion_act.objects.get(id_actividad = id, tipo = 1)
	#Se obitne idNotif
	field_name = 'id_notificacion'
	obj = Notificacion_act.objects.get(id_actividad = id, tipo = 1)
	field_value = getattr(obj, field_name)
	idNotif = field_value
	Notificacion_act_alumnoD = Notificacion_act_alumno.objects.filter(id_notificacion = idNotif)
	try:
		ActividadDocenteD.delete()
		Notificacion_actD.delete()
		for n in Notificacion_act_alumnoD:
			n.delete()
		sweetify.success(request, 'Se eliminó', text='La actividad fue eliminada exitosamente', persistent='Ok', icon="success")
	except:
		sweetify.error(request, 'No se eliminó', text='Ocurrió un error', persistent='Ok', icon="error")
	ActividadDocentes = Actividad_docente.objects.all()

	return redirect('TBC:actividadesAprendizaje')


'''
Función para retroalimentar la actividad entregada por el alumno
'''
def revisarActividad(request, id, idAlumno):
	ActividadDocente = Actividad_docente.objects.get(id_actividad = id)
	Archivos = Archivo.objects.filter(id_actividad = id)
	AlumnoS = Alumno.objects.get(id_alumno = idAlumno)
	Entrega = Entrega_actividad.objects.get(id_actividad = id, id_alumno = idAlumno)
	if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse('login'))
	usuarioLogueado = request.user

	#Si el usuario logeado es un docente tipo_usuario = 6, entonces se procede a asignar el idDocente correspondiente
	if usuarioLogueado.tipo_usuario == '6':
		try:
			#Para sacar el idDocente de la tabla de tbc con base en el registro CustomUser
			field_name = 'id_docente'
			obj = Docente.objects.get(email = request.user.email) #TODO: Cambiar last_name ya que se la haya dado más espacio
			field_value = getattr(obj, field_name)
			idDocente = field_value
		except:
			print('')
	
	#Si el usuario logeado es un alumno tipo_usuario = 7, entonces se procede a asignar el idAlumno correspondiente
	if usuarioLogueado.tipo_usuario == '7':
		try:
			#Para sacar el idAlumno de la tabla de tbc con base en el registro de CustomUser
			field_name = 'id_alumno'
			obj = Alumno.objects.get(email = request.user.email) #TODO:Cambiar last_name ya que se le haya dado más espacio
			field_value = getattr(obj, field_name)
			idAlumnoI = field_value
		except:
			print('')

	if request.method == 'POST':
		try:
			#Sólo se actualizará el registro de la Entrega (actualizando los campos de calificación, retroalimentación y calificada)
			calificacion = request.POST['calificacion']
			retroalimentacion = request.POST['retroalimentacion']
			totalOb = request.POST['totalObtenido2']
			print('entra 0')
			#calificada = True
			Entrega_actividad.objects.filter(id_actividad = id, id_alumno = idAlumno).update(calificacion = calificacion, retroalimentacion = retroalimentacion, calificada = True, totalO = totalOb)
			#Se saca el id de la notificacion (tabla notif_act_alumno) correspondiente a actualizar con el id_dc y el id_actividad (tabla notifi_act)
			print('entra 1')
			field_name = 'id_notificacion'
			obj = Notificacion_act.objects.filter(id_actividad = id, tipo = 2).last()
			field_value = getattr(obj, field_name)
			idNotificacion = field_value
			print('entra 2')
			NotifStatus = Notificacion_act_docente.objects.filter(id_notificacion = idNotificacion, id_alumno = idAlumno).update(status = 1)
			sweetify.success(request, 'Se calificó', text='La actividad fue calificada exitosamente', persistent='Ok', icon="success")
		except:
			sweetify.error(request, 'No se calificó', text='Ocurrió un error', persistent='Ok', icon="error")
		return redirect('/TBC/actividad-docente/'+id)
	return render(request, 'revisarActividad.html', {'usuario':usuarioLogueado, 'actividad':ActividadDocente, 'archivo':Archivos, 'alumno':AlumnoS, 'entrega':Entrega, }) 

'''
Función para consultar los cursos y actividades del alumno logeado
'''
def actividadAlumno (request, id):
	AlumnoI = Alumno.objects.get(id_alumno = id)
	AlumnoCursos = Alumno_curso.objects.filter(id_alumno = id)
	Cursos = Curso.objects.all()
	Modulos = Modulo.objects.all()
	ActividadAlumno = Actividad_docente.objects.all()
	NotificacionAct = Notificacion_act.objects.all()
	NotificacionActAalumno = Notificacion_act_alumno.objects.filter(id_alumno = id)
	DocenteCurso = Docente_curso.objects.all()
	#ActividadAlumno = Actividad_docente.objects.filter(id_curso = idDocente)
	if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse('login'))
	usuarioLogueado = request.user

	#Si el usuario logeado es un docente tipo_usuario = 6, entonces se procede a asignar el idDocente correspondiente
	if usuarioLogueado.tipo_usuario == '6':
		try:
			#Para sacar el idDocente de la tabla de tbc con base en el registro CustomUser
			field_name = 'id_docente'
			obj = Docente.objects.get(email = request.user.email) #TODO: Cambiar last_name ya que se la haya dado más espacio
			field_value = getattr(obj, field_name)
			idDocente = field_value
		except:
			print('')
	
	#Si el usuario logeado es un alumno tipo_usuario = 7, entonces se procede a asignar el idAlumno correspondiente
	if usuarioLogueado.tipo_usuario == '7':
		try:
			#Para sacar el idAlumno de la tabla de tbc con base en el registro de CustomUser
			field_name = 'id_alumno'
			obj = Alumno.objects.get(email = request.user.email) #TODO:Cambiar last_name ya que se le haya dado más espacio
			field_value = getattr(obj, field_name)
			idAlumnoI = field_value
		except:
			print('')
	try:
		Entregas = Entrega_actividad.objects.filter(id_alumno = id)
		return render(request, 'actividadAlumno.html', {'docenteCurso':DocenteCurso, 'usuario':usuarioLogueado, 'alumno':AlumnoI, 'alumnoCurso':AlumnoCursos, 'curso':Cursos, 'modulo':Modulos ,'actividad_docente': ActividadAlumno, 'entrega': Entregas, 'notificaciones':NotificacionAct, 'notificacion':NotificacionActAalumno, })
	except:
		print('kaka')
	return render(request, 'actividadAlumno.html', {'docenteCurso':DocenteCurso,'usuario':usuarioLogueado, 'alumno':AlumnoI, 'alumnoCurso':AlumnoCursos, 'curso':Cursos,'modulo':Modulos ,'actividad_docente': ActividadAlumno, 'notificaciones':NotificacionAct, 'notificacion':NotificacionActAalumno,})

'''
Función para la funcionalidad de toma de lista
'''
def ListasAsistencias(request):
	#La action del form en paseLista.html ejecuta un POST a la URL ligada a esta view
	if request.method == 'POST':
		#Creamos un workbook a traves de la libreria xlwt
		wb = xlwt.Workbook(encoding='utf-8')
		#A ese workbook le agregamos una sheet con las asistencias del módulo
		ws = wb.add_sheet('Lista Matematicas1')

		#Definimos las variables con las que navegaremos e imprimiremos en el archivo de excel
		row_num = 2
		font_style1 = xlwt.XFStyle()
		font_style1.font.bold = True
		#Creamos una lista con los encabezados del primer renglon
		columnasLista = ['Nombre Alumno','Matricula','Asistencia','Retardo','Justificacion']

		# A traves de un for imprimimos la lista pasada en la hoja de excel, indicando en que fila y en que columna se imprime cada cosa y con que fuente.
		for col_num in range(len(columnasLista)):
			ws.write(row_num, col_num, columnasLista[col_num], font_style1)
		
		#Repetimos proceso de encabezados
		infoGrupo = ['Módulo','Docente','Semestre','Periodo','Fecha']
		row_num=0
		for col_num in range(len(infoGrupo)):
			ws.write(row_num, col_num, infoGrupo[col_num], font_style1)
		font_style = xlwt.XFStyle()
		font_style.font.bold = False

		infoGrupoRes = ['Matematicas 1',request.user.first_name+" "+request.user.last_name,'4to Semestre','Enero - Junio 2020','04 Mayo 2020']
		row_num=1
		for col_num in range(len(infoGrupoRes)):
			ws.write(row_num,col_num,infoGrupoRes[col_num], font_style)

		#Obtenemos los alumnos (Por el momento son todos, despues se filtrará por grupoS)
		alumnos = Alumno.objects.all()
		row_num=3
		counter= 0
		asistenciaFinal = ""
		retardoFinal = ""
		justificacionFinal =""

		#Por cada alumno encontrado se evaluarán las checkboxes de la vista y dependiendo del valor se cambiarán los valores 
		for row in alumnos:
				if not request.POST.get('Asistencia'+str(counter)):
					asistenciaFinal = ""
				else:
					asistenciaFinal = "•"
				if not request.POST.get('Retardo'+str(counter)):
					retardoFinal = ""
				else:
					retardoFinal="•"
				if not request.POST.get('Justificacion'+str(counter)):
					justificacionFinal = ""
				else:
					justificacionFinal="•"
				#Imprimimos los valores finales de cada alumno
				ws.write(row_num,0,row.nombre_alumno, font_style)
				ws.write(row_num,1,row.num_matricula, font_style)
				ws.write(row_num,2,asistenciaFinal,font_style)
				ws.write(row_num,3,retardoFinal,font_style)
				ws.write(row_num,4,justificacionFinal,font_style)
				row_num+=1
				counter+=1
		#Guardamos nuestrow workbook y retornamos
		response = HttpResponse(content_type='application/ms-excel')
		response['Content_Disposition'] = 'attachment; filename="test.xls"'
		wb.save(response)
		return response


''' ================= SECCION DE LAS VIEWS PARA EL MANEJO DE MODULOS EN TBC =========================''' 
def nuevoModulo(request):
	semestres = Semestre.objects.all()
	areas_disc = Area_disciplinar.objects.all()
	Modulos = Modulo.objects.all()
	if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse('login'))
	usuarioLogueado = request.user
	return render(request, 'nuevoModulo.html',{'semestres': semestres,'areas_disc':areas_disc,'modulos':Modulos,'usuario':usuarioLogueado})

def nuevoModuloInsertar(request):
	if request.is_ajax:
		moduloNuevo = Modulo(nombre_modulo = request.GET.get('nombre'), semestre_modulo = Semestre.objects.get(id_semestre=request.GET.get('semestre')), areadisciplinar_modulo = Area_disciplinar.objects.get(id_areadisciplinar=request.GET.get('AD')), creditos_modulo = request.GET.get('creditos'))
		moduloNuevo.save()
		data = serializers.serialize("json",Modulo.objects.filter(nombre_modulo=request.GET.get('nombre')))
		return JsonResponse(data,safe=False)

def nuevaUnidad(request):
	if request.is_ajax:
		print('============='+request.GET.get('moduloDeLaUnidad')+'    lol=========')
		unidadNueva = Unidad_modulo(nombre_unidad = request.GET.get('nombreUnidad'), id_modulo_unidad = Modulo.objects.get(id_modulo=request.GET.get('moduloDeLaUnidad')), proposito_unidad = "")
		unidadNueva.save()
		data = serializers.serialize("json",Unidad_modulo.objects.filter(nombre_unidad=request.GET.get('nombreUnidad')))
		return JsonResponse(data,safe=False)

def nuevoApes(request):
	if request.is_ajax:
		apesNuevo = Aprendizaje_esperado_modulo(aprendizaje_esperado = request.GET.get('apesDeLaUnidad'), unidad_aprendizaje_esperado = Unidad_modulo.objects.get(id_unidad=request.GET.get('nombreUnidad')), modulo_aprendizaje_esperado = Modulo.objects.get(nombre_modulo=request.GET.get('modulo')))
		apesNuevo.save()
		data = serializers.serialize("json",Aprendizaje_esperado_modulo.objects.filter(aprendizaje_esperado=request.GET.get('apesDeLaUnidad')))
		return JsonResponse(data,safe=False)

def getAPES(request,idNombre):
	if request.is_ajax:
		data = serializers.serialize("json",Aprendizaje_esperado_modulo.objects.filter(unidad_aprendizaje_esperado = idNombre))
		return JsonResponse(data,safe=False)

def deleteUnidad(request,idNombre):
	if request.is_ajax:
		deleteAPES = Aprendizaje_esperado_modulo.objects.filter(unidad_aprendizaje_esperado = idNombre).delete()
		deletetionUnidad = Unidad_modulo.objects.filter(id_unidad=idNombre).delete()
		return JsonResponse("deleted",safe=False)

def getUnidades(request):
	if request.is_ajax:
		data = serializers.serialize("json",Unidad_modulo.objects.filter(id_modulo_unidad__in=Subquery(Modulo.objects.filter(nombre_modulo=request.GET.get('idNombre')).values('id_modulo'))))
		return JsonResponse(data,safe=False)

def updateUnidad(request):
	if request.is_ajax:
		updatedUnidad = Unidad_modulo.objects.filter(id_unidad = request.GET.get('idNombre')).update(nombre_unidad = request.GET.get('nombreUnidad'))
		return JsonResponse("Updated",safe=False)

def deleteAPES(request):
	if request.is_ajax:
		print(request.GET.get('aprendizajeActual'))
		deleteAPES = Aprendizaje_esperado_modulo.objects.filter(id = request.GET.get('aprendizajeEsperado').split('-')[1]).delete()
		return JsonResponse("deleted",safe=False)

def updateAPES(request):
	if request.is_ajax:
		updatedUnidad = Aprendizaje_esperado_modulo.objects.filter(id = request.GET.get('aprendizajeActual').split('-')[1]).update(aprendizaje_esperado = request.GET.get('aprendizajeNuevo'))
		return JsonResponse("Updated",safe=False)

def updPropUnidad(request):
	if request.is_ajax:
		updatedUnidad = Unidad_modulo.objects.filter(Q(id_unidad = request.GET.get('unidad')) & Q(id_modulo_unidad=request.GET.get('modulo'))).update(proposito_unidad = request.GET.get('proposito'))
		return JsonResponse("Updated proposito de la unidad",safe=False)

def updArchivo(request):
	if request.is_ajax:
		if request.method == 'POST':
			doc = request.FILES 
			updatedModulo = Modulo.objects.filter(id_modulo=request.POST.get('modulo')).update(pdf_modulo = request.FILES['archivo'])
			return JsonResponse("Updated pdf de la unidad",safe=False)

def getPropUnidad(request):
	if request.is_ajax:
		propUnidad = serializers.serialize("json",Unidad_modulo.objects.filter(Q(id_unidad = request.GET.get('unidad')) & Q(id_modulo_unidad=request.GET.get('modulo'))))
		return JsonResponse(propUnidad,safe=False)
		
''' ================= FINAL DE LA SECCION DE LAS VIEWS PARA EL MANEJO DE MODULOS EN TBC =========================''' 

#Función para realizar la entrega por parte del alumno
def entregaAlumno(request, id, idAlumno):
	if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse('login'))
	usuarioLogueado = request.user

	#Si el usuario logeado es un docente tipo_usuario = 6, entonces se procede a asignar el idDocente correspondiente
	if usuarioLogueado.tipo_usuario == '6':
		try:
			#Para sacar el idDocente de la tabla de tbc con base en el registro CustomUser
			field_name = 'id_docente'
			obj = Docente.objects.get(email = request.user.email) #TODO: Cambiar last_name ya que se la haya dado más espacio
			field_value = getattr(obj, field_name)
			idDocente = field_value
		except:
			print('')
	
	#Si el usuario logeado es un alumno tipo_usuario = 7, entonces se procede a asignar el idAlumno correspondiente
	if usuarioLogueado.tipo_usuario == '7':
		try:
			#Para sacar el idAlumno de la tabla de tbc con base en el registro de CustomUser
			field_name = 'id_alumno'
			obj = Alumno.objects.get(email = request.user.email) #TODO:Cambiar last_name ya que se le haya dado más espacio
			field_value = getattr(obj, field_name)
			idAlumnoI = field_value
		except:
			print('')

	c = 0
	Alumnos = Alumno.objects.all()
	ActividadDocente = Actividad_docente.objects.get(id_actividad = id)
	Entregas = Entrega_actividad.objects.filter(id_actividad = id)
	Archivos = Archivo.objects.filter(id_actividad = id)
	Cursos = Curso.objects.all()
	Modulos = Modulo.objects.all()
	try:
		Docentes = Docente.objects.filter(id_docente = idDocente)
	except:
		#Se debe de sacar el id_docente para hacer las inserciones
		#Se quiere obtener el id_docente haciendo la relacion con la actividad
		field_name = 'id_docente'
		obj = Actividad_docente.objects.get(id_actividad = id)
		field_value = getattr(obj, field_name)
		idDocente = field_value
		Docentes = Docente.objects.filter(id_docente = idDocente)
	
	try:
		Entrega = Entrega_actividad.objects.get(id_actividad = id, id_alumno = idAlumno)
		return render(request, 'entregaAlumno.html', {'usuario':usuarioLogueado, 'actividad':ActividadDocente, 'docente':Docentes, 'alumno':Alumnos, 'entrega':Entregas , 'archivo':Archivos, 'curso':Cursos, 'entregaA': Entrega })
	except:
		print('')
	if request.method == 'POST':
		nombreArchivos = ''
		try:
			idActividad = id
			#TODO: Realizar la actualización de archivos ya subidos
			#Ciclo para recorrer los archivos seleccionados y guardarlos (recursos)
			for afile in request.FILES.getlist('recursoAlumno'):
				#myfile = afile
				#fs = FileSystemStorage("media/TBC/Alumno")
				#filename = fs.save(myfile.name, myfile)
				#uploaded_file_url = fs.url(filename)
				nombreArchivos += afile.name + '\n'

				#Se obtiene el id del archivo actual para incrementar en 1 e insertarlo
				field_name = 'id_archivo'
				obj = Archivo.objects.last()
				field_value = getattr(obj, field_name)
				idArchivo = field_value + 1

				descripcion = request.POST.getlist('descRecurso')
				url = 'https://storage.googleapis.com/plataformase.appspot.com/TBC/archivos/entregas'+afile.name
				ArchivoNuevo = Archivo(id_archivo = idArchivo, nombre_archivo = afile.name, descripcion = descripcion[c], tipo_archivo = 'Entrega', id_actividad = idActividad, url= url, id_alumno = idAlumno)
				ArchivoNuevo.archivo = afile
				ArchivoNuevo.save()
				c += 1
			comentario = request.POST['comentario']
			curso = request.POST['curso']
			date_joined = datetime.now()
			formatted_datetime = formats.date_format(date_joined, "SHORT_DATETIME_FORMAT")	
			fechaHoraSubida = formatted_datetime
			nombreActividad = request.POST['nombreAct']
			#Para sacar el ultimo id registrado y sumarle 1
			# field_name = 'id_entrega'
			# obj = Entrega_actividad.objects.last()
			# field_value = getattr(obj, field_name)
			# idEntrega = field_value + 1
			EntregaNueva = Entrega_actividad(nombre_actividad = nombreActividad, fecha_hora_subida = fechaHoraSubida, id_alumno = idAlumno, id_actividad = id ,comentario = comentario, calificada = False, entregada = True)
			
			#TODO: Sólo insertar 1 registro al entregar una actividad, si ya existe no se inserta y solo se relaciona el alumno
			#Se obtiene el campo id_dc de la tabla de Docente_curso
			field_name = 'id_dc'
			obj = Docente_curso.objects.get(id_docente = idDocente, id_curso = curso)
			field_value = getattr(obj, field_name)
			idDc = field_value
			#Aqui ya se tienen los datos a insertar, se procede a comprobar si ya existe uno insertado
			notifI = Notificacion_act.objects.filter(id_dc = idDc, id_actividad = id, mensaje = 'Nueva entrega', tipo = 2).count()
			if notifI > 0:
				print('ya hay uno')
				field_name = 'id_notificacion'
				obj = Notificacion_act.objects.get(id_dc = idDc, id_actividad = id, tipo = 2)
				field_value = getattr(obj, field_name)
				idNotif = field_value
				print(idNotif)
				nuevaNotifD = Notificacion_act_docente(id_docente = idDocente, status = 0, id_notificacion = idNotif, id_alumno = idAlumno, id_dc = idDc, tipo = 2)
				
			else:
				notifAct = Notificacion_act(id_dc = idDc, id_actividad = id, mensaje = 'Nueva entrega', tipo = 2)
				notifAct.save()
				#Se inserta la notificación relacionandola al id de la notificacion
				#Se insertan los campos id_docente, id_notif y el id_alumno
				field_name = 'id_notificacion'
				obj = Notificacion_act.objects.last()
				field_value = getattr(obj, field_name)
				idNotif = field_value
				print(idNotif)
				nuevaNotifD = Notificacion_act_docente(id_docente = idDocente, status = 0, id_notificacion = idNotif, id_alumno = idAlumno, id_dc = idDc, tipo = 2)
			
			#Se actualiza la notificación de actividadNueva y ponerla en leída
			#Se saca el id de la notificacion (tabla notif_act_alumno) correspondiente a actualizar con el id_dc y el id_actividad (tabla notifi_act)
			field_name = 'id_notificacion'
			obj = Notificacion_act.objects.get(id_actividad = id, tipo = 1)
			field_value = getattr(obj, field_name)
			idNotificacion = field_value
			NotifStatus = Notificacion_act_alumno.objects.filter(id_alumno = idAlumno, id_notificacion = idNotificacion).update(status = 1)
			
			#No existen errores, se proceden a guardar
			EntregaNueva.save()
			nuevaNotifD.save()
			sweetify.success(request, 'Se entregó', text='La actividad fue entregada exitosamente', persistent='Ok', icon="success")
		except Exception as e:
			print(e)
			sweetify.error(request, 'No se entregó', text='Ocurrió un error', persistent='Ok', icon="error")
		return redirect('/TBC/actividad-alumno/'+str(idAlumno))

	return render(request, 'entregaAlumno.html', {'usuario':usuarioLogueado, 'actividad':ActividadDocente, 'docente':Docentes, 'alumno':Alumnos, 'entrega':Entregas , 'archivo':Archivos, 'curso':Cursos, 'modulo':Modulos })#'entregaA':Entrega}) 


'''
Función para relacionar un módulo con un docente y ese módulo-docente con un grupo de alumnos (por semestres)
'''
def relacionarModulo(request):
	if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse('login'))
	usuarioLogueado = request.user

	#Si el usuario logeado es un docente tipo_usuario = 6, entonces se procede a asignar el idDocente correspondiente
	if usuarioLogueado.tipo_usuario == '6':
		try:
			#Para sacar el idDocente de la tabla de tbc con base en el registro CustomUser
			field_name = 'id_docente'
			obj = Docente.objects.get(email = request.user.email) #TODO: Cambiar last_name ya que se la haya dado más espacio
			field_value = getattr(obj, field_name)
			idDocente = field_value
		except:
			print('')
	
	#Si el usuario logeado es un alumno tipo_usuario = 7, entonces se procede a asignar el idAlumno correspondiente
	if usuarioLogueado.tipo_usuario == '7':
		try:
			#Para sacar el idAlumno de la tabla de tbc con base en el registro de CustomUser
			field_name = 'id_alumno'
			obj = Alumno.objects.get(email = request.user.email) #TODO:Cambiar last_name ya que se le haya dado más espacio
			field_value = getattr(obj, field_name)
			idAlumnoI = field_value
		except:
			print('')
	Docentes = Docente.objects.filter(cct = usuarioLogueado.last_name)
	Alumnos = Alumno.objects.filter(cct = usuarioLogueado.last_name)
	Modulos = Modulo.objects.all()
	DocenteModulo = Docente_curso.objects.all()
	# cct del logincustomuser = last_name print(usuarioLogueado.last_name) TODO: Cambiar a la relación que tenga Diana al dar de alta la institución
	#Para relacionar un módulo con un docente
	if request.method == 'POST':
		bandera = request.POST['bandera']
		#False para relacionar módulo con un docente
		if bandera == 'False':
			try:
				idDocente = request.POST['docente']
				idModulo = request.POST['modulo']
				print('x', idModulo, idDocente)
				try:
					field_name = 'id_dc'
					obj = Docente_curso.objects.last()
					field_value = getattr(obj, field_name)
					id_Dc = field_value + 1
				except:
					id_Dc = 1
				nuevoDocenteMod = Docente_curso(id_dc = id_Dc, id_curso = idModulo, id_docente = idDocente)
				nuevoDocenteMod.save()
				sweetify.success(request, 'Relación realizada', text='El docente fue relacionado al módulo seleccionado', persistent='Ok', icon="success")
			except Exception as e:
				print(e)
		elif bandera == 'True':
			#True para relacionar alumnos con un modulo-docente
			alumnosL = request.POST.getlist('nombreAlumnoTabla') or None
			id_alumnoL = request.POST.getlist('id_alumnoL') or None
			idDocMod = request.POST['docenteModulo']
			idx = 0
			for al in alumnosL:
				if not request.POST.get('alumnoModulo'+str(idx)):
					cursando = False
				else:
					cursando = True
				#Se recorren los alumnos que están en la tabla ya obteniendo si está checkeado el checkbox o no
				#print('id del curso: ', idDocMod)
				#print(id_alumnoL[idx], ' - ', cursando)
				#Se guarda en la tabla alumnoCurso
				try:
					field_name = 'id_ac'
					obj = Alumno_curso.objects.last()
					field_value = getattr(obj, field_name)
					id_Ac = field_value + 1
				except:
					id_Ac = 1
				#Insertar solo los que sean cursando = True
				if cursando == True:
					try:
						nuevoAlCurso = Alumno_curso(id_ac = id_Ac, id_dc = idDocMod, id_alumno = id_alumnoL[idx] )
						nuevoAlCurso.save()
						print('insertao segun', id_alumnoL[idx])
						sweetify.success(request, 'Relación realizada', text='Los alumnos fueron relacionado al módulo seleccionado', persistent='Ok', icon="success")
					except:
						sweetify.error(request, 'No se realizó la operación', text='Ocurrió un error', persistent='Ok', icon="error")
				else:
					print('')
				idx += 1

	return render(request, 'relacionarModulo.html', {'usuario':usuarioLogueado, 'docente':Docentes, 'modulo':Modulos, 'alumno':Alumnos, 'docenteModulo':DocenteModulo }) 

#Fin