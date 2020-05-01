from django.urls import path
from .views import *

urlpatterns = [
   path('Resultados', resultadosTBC, name='ResultadosExamenTBC'),
<<<<<<< HEAD
=======
   path('', homePage, name='HomePage')
>>>>>>> 336c7c9c5b3edb1eb969590ceadded3e3d9095b1
]