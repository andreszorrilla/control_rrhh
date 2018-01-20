from django.conf.urls import patterns, url
from .views import *
from django.contrib.auth.decorators import permission_required

urlpatterns = patterns('',

                       #Solicitud
                       url(
                           regex=r'^solicitud/listar$',
                           view=SolicitudList.as_view(),
                           name="solicitud_list"
                       ),

                       url(
                           regex=r'^solicitud/create$',
                           view=SolicitudCreate.as_view(),
                           name="solicitud_create"
                       ),

                       url(
                           regex=r'^solicitud/detail/(?P<pk>\d+)$',
                           view=SolicitudDetail.as_view(),
                           name="solicitud_detail"
                       ),
                       url(
                           regex='^solicitud/anular/(?P<pk>\d+)$',
                           view=SolicitudAnular.as_view(),
                           name='solicitud_anular'
                       ),


                       # Busquedas
                       url(
                           regex='^solicitud/buscar_funcionario/',
                           view=JSONSolicitudBuscarFuncionario.as_view(),
                           name='solicitud_buscar_funcionario'
                       ),


                       #Ajustes
                       url(
                           regex=r'^ajustes$',
                           view=AjustesList.as_view(),
                           name="ajustes_vacaciones_list"
                       ),

                       url(
                           regex=r'^ajustes/detail/(?P<pk>\d+)$',
                           view=AjustesDetail.as_view(),
                           name="ajustes_vacaciones_detail"
                       ),

                       url(
                           regex=r'^ajustes/detail/create/',
                           view=permission_required('vacaciones.add_periodo')(AjustesDetailCreate.as_view()),
                           name="ajustes_vacaciones_detail_create"
                       ),

                       url(
                           regex=r'^ajustes/detail/update/(?P<pk>\d+)$',
                           view=AjustesDetailUpdate.as_view(),
                           name="ajustes_vacaciones_detail_update"
                       ),
                       url(
                           regex='^ajustes/detail/get_dias_libres/',
                           view=JSONObtenerCantidadDias.as_view(),
                           name='get_dias_libres'
                       ),
                       url(
                           regex=r'^buscador_funcionario/(?P<cedula>\d+)$',
                           view = JSONFuncionarioPorCelula.as_view(),
                           name="aaaa"
                        ),
                       url(
                           regex=r'^consulta$',
                           view=ConsultaList.as_view(),
                           name="consulta_vacaciones_list"
                       ),


)

