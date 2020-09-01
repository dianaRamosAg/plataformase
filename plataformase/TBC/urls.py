from django.urls import path
from .views import *

urlpatterns = [
   path('Resultados', resultadosTBC, name='ResultadosExamenTBC'),

   path('', homePage, name='HomePage')

]