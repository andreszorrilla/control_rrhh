from django.conf.urls import patterns, url

from .views import *
from django.contrib.auth.decorators import login_required, permission_required


urlpatterns = patterns('',
                       url(
                           regex=r'^antiguedad$',
                           view=permission_required('antiguedad.can_change')(AntiguedadList.as_view()),
                           name="antiguedad_list"
                       ),
                       url(
                           regex=r'^antiguedad/create$',
                           view=permission_required('antiguedad.can_add')(AntiguedadCreate.as_view()),
                           name="antiguedad_create"
                       ),
                       url(
                           regex=r'^antiguedad/detail/(?P<pk>\d+)$',
                           view=permission_required('antiguedad.can_change')(AntiguedadDetail.as_view()),
                           name="antiguedad_detail"
                       ),
                       url(
                           regex=r'^antiguedad/update/(?P<pk>\d+)$',
                           view=permission_required('antiguedad.can_change')(AntiguedadUpdate.as_view()),
                           name="antiguedad_update"
                       ),

                       #Funcionario
                       url(
                           regex=r'^funcionario/listar',
                           view=login_required( FuncionarioList.as_view() ),
                           name="funcionario_list"
                       ),

                       url(
                           regex=r'^funcionario/create',
                           view=login_required( FuncionarioCreate.as_view() ),
                           name="funcionario_create"
                       ),

                       url(
                           regex=r'^funcionario/detail/(?P<pk>\d+)$',
                           view=login_required( FuncionarioDetail.as_view() ),
                           name="funcionario_detail"
                       ),
                       url(
                           regex=r'^funcionario/update/(?P<pk>\d+)$',
                           view=login_required( FuncionarioUpdate.as_view() ),
                           name="funcionario_update"
                       ),


                       url(
                           regex='^funcionario/update_estado/(?P<pk>\d+)$',
                           view=login_required( FuncionarioUpdateEstado.as_view() ),
                           name='funcionario_update_estado'
                       ),

                       #Parametros
                       url(
                           regex='^parametro/(?P<pk>\d+)$',
                           view=permission_required('parametro.can_change')( ParametroDetail.as_view() ),
                           name='parametro_detail'
                       ),

                       url(
                           regex='^parametro/update/(?P<pk>\d+)$',
                           view=permission_required('parametro.can_change')( ParametroUpdate.as_view() ),
                           name='parametro_update'
                       ),

                       # Secciones
                       url(
                           regex=r'^seccion/listar',
                           view=login_required( SeccionList.as_view() ),
                           name="seccion_list"
                        ),

                       url(
                           regex=r'^seccion/form',
                           view=login_required( SeccionCreate.as_view() ),
                           name="seccion_form"
                        ),

                       url(
                           regex=r'^seccion/detail/(?P<pk>\d+)$',
                           view=login_required( SeccionDetail.as_view() ),
                           name="seccion_detail"
                        ),

                       url(
                           regex=r'^seccion/update/(?P<pk>\d+)$',
                           view=login_required( SeccionUpdate.as_view() ),
                           name="seccion_update"
                        ),

                       url(
                           regex=r'^seccion/delete/(?P<pk>\d+)$',
                           view=login_required( SeccionDelete.as_view() ),
                           name="seccion_delete"
                        ),


                       ## Cargos


                       url(
                           regex=r'^cargo/create',
                           view=login_required( CargoCreate.as_view() ),
                           name="cargo_create"
                       ),


                       url(
                           regex=r'^cargo/listar',
                           view=login_required( CargoList.as_view() ),
                           name="cargo_list"
                        ),

                       url(
                           regex=r'^cargo/form',
                           view=login_required( CargoCreate.as_view() ),
                           name="cargo_form"
                        ),

                       url(
                           regex=r'^cargo/detail/(?P<pk>\d+)$',
                           view=login_required( CargoDetail.as_view() ),
                           name="cargo_detail"
                        ),

                       url(
                           regex=r'^cargo/update/(?P<pk>\d+)$',
                           view=login_required( CargoUpdate.as_view() ),
                           name="cargo_update"
                        ),

                       url(
                           regex=r'^cargo/delete/(?P<pk>\d+)$',
                           view=login_required( CargoDelete.as_view() ),
                           name="cargo_delete"
                        ),

                       url(
                           regex=r'^cargo/seccion/(?P<id_seccion>\d+)$',
                           view=login_required( JSONCargosBySeccion.as_view() ),
                           name="cargo_by_seccion"
                        ),

                       url(
                           regex=r'^buscador',
                           view= Buscador.as_view() ,
                           name="buscador"
                        ),

)

