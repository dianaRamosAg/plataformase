# Plataforma de servicios digitales de la Subsecretaría de Educación Media Superior, Superior  e Investigación Científica y Tecnológica 

>Se encuentran de manera centralizada aplicaciones que han sido desarrolladas en la SSEMSSICyT y otras que están en proceso, de las cuales se consideran hasta el momento las siguientes: Generación de turnos de RVOE, SIG, TBC, Autorización de exámenes a títulos y registro de sinodales. 

### Requerimientos para ejecutar 🚀
- Python -> 3.7
- Django -> 2.2
- PostgresSQL 11-12
- PgAdmin 4
- Entorno virtual 

### Agregar aplicaciones terminadas ó incluir desde el inicio del desarrollo de estas.📋
#### Crear la aplicación dentro del proyecto de plataforma
``` python manage.py startapp nombre_aplicación ```
- Agregar la nueva aplicación al settings en **INSTALLED_APPS**
- Agregar las rutas de la aplicación al archivo **urls** del proyecto plataforma
- Realizar las migraciones del proyecto de todas las aplicaciones que contiene:

``` python manage.py makemigrations nombre_aplicación ```

``` python manage.py migrate nombre_aplicación ```

- Correr el servidor para verificar funcionamiento del sistema ``` python manage.py runserver```⚙️
#### En caso de ser una aplicación externa del proyecto se realizan los mismos pasos a excepción de ''crear la aplicación''
- Guardando aplicación dentro del proyecto


# Configuración del proyecto con Apache con WSGI

### Pre-requisitos 📋

Para seguir estos pasos de configuración de apache con WSGI se utilizó:

* Ubuntu 18.04
* Django 2.2.1
* PostgreSQL 11
* Apache 2.4
* [Anaconda para Python 3.7 ](https://docs.anaconda.com/anaconda/install/linux/)

### Pasos a seguir:

1. Instalar las librerías requeridas

Vamos a descargar e instalar paquetes de repositorios de Ubuntu que son necesarios para Django. Los siguientes son los comandos:

```
sudo apt-get update

sudo apt-get install python3-pip apache2 libapache2-mod-wsgi-py3
```
El comando anterior instalará Apache2 the Web Server, mod_wsgi para comunicarse e interactuar con nuestra aplicación Django y pip3, el administrador de paquetes de Python para descargar herramientas relacionadas con Python.

También necesitamos instalar el paquete de psycopg2 que nos servirá como controlador para conectar nuestra aplicación con la base de datos de PostgreSQL. Para esto utilizamos el siguiente comando:
```
sudo apt-get install python3-psycopg2
```

2. Clonar el repositorio

Para reducir la ruta, se recomienda que se clone el repositorio en la raíz de tu carpeta personal (en este tutorial se utilizará esta opción).

Si ya tienes clonado el repositorio también se puede copiar el mismo a la raíz (con el comando _cp -r path-origen path-destino_) o utilizar el mismo directorio donde ya está clonado.

3. Crear el ambiente con anaconda e instalar los paquetes necesarios

Creamos un ambiente de Python 3.7.3 con anaconda ejecutando el siguiente comando:

```
conda create -n pyenv python=3.7.3
```

**Nota:** puedes cambiar <_pyenv_> por el nombre que te sea más fácil de recordar para activar del ambiente de anaconda.

Una vez que se termine de instalar activamos el ambiente virtual:

```
conda activate pyenv
```

Ahora que tenemos instalado y activado nuestro ambiente con anaconda, debemos instalar los paquetes necesarios para nuestro proyecto utilizando el siguiente comando:

```
sudo pip3 install -r requirements.txt
```

**Nota:** recuerda que debes de estar en la ruta donde tienes el archivo requirements.txt o debes de colocar la ruta de donde la tienes ( _path/requirements.txt_ ).

4. Configuración del proyecto

La primer acción que siempre debemos de tener en cuenta en nuestros archivos de proyectos creados es cambiar el archivo settings.py para configurar la ubicación de archivos estaticos y la media. Abra el archivo settings.py:
```
sudo gedit <path>/settings.py
```

En la parte final del archivo settings.py, vamos a agregar el código de Python para configurar el directorio de archivos estáticos y los de media:
```
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

Sin cerrar el archivo de settings.py debes modificar la configuración de la base de datos:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        ...
    }
}
```

Añadimos la URL a utilizar en la lista **ALLOWED_HOSTS** (esta ruta la configuraremos más adelante en apache) y desactivamos el debug para que ya no se muestren los errores en pantalla:
```
DEBUG = False

ALLOWED_HOSTS = ['plataformase.localhost']
```
Ahora debemos hacer las migraciones. En la ruta donde se encuentra el archivo manage.py ejecutamos el siguiente código:
```
python3 manage.py makemigrations
python3 manage.py migrate
```

Creamos el super usuario para el proyecto:
```
python3 manage.py createsuperuser
```

Podemos reunir todo el contenido estático en la ubicación del directorio que configuramos ordenando:
```
python3 manage.py collectstatic
```

Una vez hecho esto desactivamos el ambiente virtual
```
deactivate
```

5. Desplegando la aplicación de Django en el servidor de Apache
```
sudo nano /etc/apache2/sites-available/plataformase.conf
```

**Nota:** puedes cambiar el nombre del archivo _plataformase.conf_ por el de tu preferencia dejando siempre la extención ".conf".

Añade el siguiente texto al archivo plataformase.conf
```
WSGIRestrictEmbedded On
<VirtualHost *:80>
	ServerAdmin admin@plataformase.localhost
	ServerName plataformase.localhost
	ServerAlias www.plataformase.localhost

	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined

	Alias /robots.txt /home/user/plataformase/static/robots.txt
	Alias /favicon.ico /home/user/plataformase/static/favicon.ico

	Alias /static /home/user/plataformase/static
	<Directory /home/user/plataformase/static>
		Require all granted
	</Directory>

	Alias /media /home/user/plataformase/media
	<Directory /home/user/plataformase/media>
		Require all granted
	</Directory>

	<Directory /home/user/plataformase/plataformase>
		<Files wsgi.py>
			Require all granted
		</Files>
	</Directory>

	WSGIScriptAlias / /home/user/plataformase/plataformase/wsgi.py

	WSGIDaemonProcess plataformase python-path=/home/user/plataformase:/home/user/anaconda3/envs/pyenv/lib/python3.7/site-packages
	WSGIProcessGroup plataformase
	WSGIApplicationGroup %{GLOBAL}
</VirtualHost>
```

**Nota:** Al realizar esto debes de tener en cuenta lo siguiente:

* La ruta _/home/user/plataformase/_ es la ruta que contiene el archivo "manage.py". Basate en esto para ajustar el resto de las rutas con las que vas propias.
* En el archivo "plataformase.conf", mantenemos la URL del proyecto como plataformase.localhost. Si quieres esto lo puedes cambiar por la url de tu preferencia. Si no lo configuras debes cambiar ALLOWED_HOST (en settings.py) a '*'.
* _user_ por tu nombre de usuario. Si desconoces tu nombre de usuario puedes obtenerlo introduciendo el siguiente código en la terminal:
```
whoami
```

Al finalizar esta configuración guardamos y salimos del documento.

#### Activa el archivo Virtual Host para el projecto de Django

Una vez creado el archivo "plataformase.conf", ahora necesitamos activar el archivo virtual host con los siguientes comandos:
```
cd /etc/apache2/sites-available
sudo a2dissite 000-default.conf
sudo a2ensite plataformase.conf
```

Ahora configuraremos el archivo de host locales. Esto es opcional pero recomendado.
```
sudo nano /etc/hosts
```

Y agregue la siguiente línea al final del archivo y guardela:
```
127.0.0.1 plataformase.localhost
```
Con esto ahora podrás acceder a tu proyecto utilizando la url http://plataformase.localhost/

6. Corrigiendo el error __Django stops working with RuntimeError: populate() isn't reentrant__

Esto es causado por un error en la configuración de Django en alguna parte. Para corregirlo debemos de ir a la ruta _home/user/anaconda3/envs/pyenv/lib/python3.7/site-packages/django/apps/_ y abrimos el archivo _registry.py_ buscamos las lineas:
```
if self.loading:
    # Prevent reentrant calls to avoid running AppConfig.ready()
    # methods twice.
    raise RuntimeError("populate() isn't reentrant")
```
Y la reemplazamos por:
```
if self.loading:
    # Prevent reentrant calls to avoid running AppConfig.ready()
    # methods twice.
    self.app_configs = {}
```

7. Eliminando algunos errores de permisos
```
sudo ufw allow 'Apache Full'

sudo chown :www-data /home/user/plataformase
```

Verifica tu archivo de Apache para asegurarse que no tienes errores de sintaxis:
```
sudo apache2ctl configtest
```
Si la salida tiene "Syntax OK" lo que significa que no hay error y que todo esta trabajando correctamente.

Ahora reiniciamos el servidor de apache para que los cambios surtan efecto.
```
sudo service apache2 restart
```

Y listo. Todo esta hecho, ahora solo ingresa a la url del proyecto (http://plataformase.localhost/).