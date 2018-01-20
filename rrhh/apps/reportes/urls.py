__author__ = 'leonel'
from django.conf.urls import patterns, url
from .views import Main, Funcionarios, Solicitudes
import views

urlpatterns = patterns('',
               
                       #Funcionariros

                       url(
                           regex=r'^funcionarios/main$',
                           view=Main.as_view(),
                           name="reportes_main"
                       ),

                       url(
                           regex=r'^funcionarios/list',
                           view=Funcionarios.as_view(),
                           name="reportes_funcionarios_list"
                       ),
                       url(
                           regex=r'^funcionarios/list',
                           view=Funcionarios.as_view(),
                           name="reportes_funcionarios_list"
                       ),
                       url(
                           regex=r'^solicitud/(?P<pk>\d+)$',
                           view=Solicitudes.as_view(),
                           name="solicitud"
                       ),

                       url(r'^list$', Main.as_view()),

)

