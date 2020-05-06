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

