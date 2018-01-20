from django.conf.urls import patterns, url
from .views import *
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required, permission_required
from . import views



urlpatterns = patterns('',

                       #Solicitud
                       url(
                           regex=r'^marcaciones$',
                           view=permission_required('biometrico.change_marcacion')(MarcacionList.as_view()),
                           name="marcaciones_list"
                       ),
                       #Solicitud
						    url(
						        r'^carga_marcaciones/$', 
						        view=views.carga_marcaciones,
						        name='carga_marcaciones'
						    ),
)

