from django.conf.urls import patterns, url
from apps.licencias.views import *

urlpatterns = patterns('',
    url(r'^$', 
    	LicenciaListView.as_view(), 
    	name='licencia_list'
    ),

    url(r'^form$',
    	LicenciaCreate.as_view(), 
    	name='licencia_form'
    ),

    url(regex='^obtener_motivo/',
        view=JSONObtenerMotivo.as_view(),
        name='licencias_obtener_motivo'
    ),
    url(
        regex=r'^licencia/detail/(?P<pk>\d+)$',
        view=LicenciaDetail.as_view(),
        name="licencia_detail"
    ),
    url(regex='^cargar_motivo/',
        view=MotivoAjaxCreate.as_view(),
        name='licencias_cargar_motivo'
    ),
    url(regex='^crear_fecha_final',
        view=CreateFechaFinalLicencia.as_view(),
        name="crear_fecha_final_licencia"
    ),
    url(regex='^licencias/motivo',
        view=MotivoListView.as_view(),
        name='motivo_list'
    ),
    url(regex='^motivo/form/',
        view=MotivoViewForm.as_view(),
        name='motivo_form'
    ),
    url(regex=r'^motivo/edit/(?P<pk>\d+)$',
        view=MotivoViewForm.as_view(),
        name='motivo_edit'
    ),

    url(regex=r'^motivo/delete/(?P<pk>\d+)$',
        view=MotivoDeleteView.as_view(),
        name='motivo_delete'
    ),

    url(regex=r'^licencia/delete/(?P<pk>\d+)$',
        view=LicenciaDeleteView.as_view(),
        name='licencia_delete'
    ),
    url(regex='^feriados',
        view=FeriadoListView.as_view(),
        name='feriado_list'
    ),
    url(regex='^feriado/form',
        view=FeriadoViewForm.as_view(),
        name='feriado_form'
    ),

    url(regex='^feriado/edit/(?P<pk>\d+)$',
        view=FeriadoViewForm.as_view(),
        name='feriado_edit'
    ),

    url(regex='^feriado/detail/(?P<pk>\d+)$',
        view=FeriadoDetail.as_view(),
        name='feriado_detail'
    ),

    url(regex='^feriado/delete/(?P<pk>\d+)$',
        view=FeriadoDeleteView.as_view(),
        name='feriado_delete'
    ),

    url(regex='^feriado/json',
        view=JSONFeriados.as_view(),
        name='feriado_json'
    ),
)