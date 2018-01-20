from django.conf.urls import patterns, url
from .views import *
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = patterns('',
                        url(
                            regex=r'^$',
                            view=permission_required('justificaciones.change_justificacion')(JustificacionList.as_view()),
                            name="justificaciones_list"
                        ),
                        url(
                            regex=r'^(?P<pk>\d+)$',
                            view=permission_required('justificaciones.change_justificacion')(JustificacionDetail.as_view()),
                            name="justificacion_detail"
                        ),
                        url(
                            r'^new/$', 
                            view=permission_required('justificaciones.change_justificacion')(JustificacionCreate.as_view()),
                            name='justificacion_new'
                        ),
                        url(
                            r'(?P<pk>[0-9]+)/edit/$', 
                            view=permission_required('justificaciones.change_justificacion')(JustificacionUpdate.as_view()),
                            name='justificacion_edit'
                        ),


                        url(
                            r'(?P<pk>[0-9]+)/delete/$', 
                            view=permission_required('justificaciones.change_justificacion')(JustificacionDelete.as_view()),
                            name='justificacion_delete'
                        ),

                        url(
                            regex=r'^motivos/$',
                            view=permission_required('justificaciones.change_justificacion')(MotivoJustificacionList.as_view()),
                            name="motivos_justificaciones_list"
                        ),
                        url(
                            regex=r'^motivos/(?P<pk>\d+)$',
                            view=permission_required('justificaciones.change_justificacion')(MotivoJustificacionDetail.as_view()),
                            name="motivo_justificacion_detail"
                        ),
                        url(
                            r'^motivos/new/$', 
                            view=permission_required('justificaciones.change_justificacion')(MotivoJustificacionCreate.as_view()),
                            name='motivo_justificacion_new'
                        ),
                        url(
                            r'^motivos/edit/(?P<pk>[0-9]+)/$', 
                            view=permission_required('justificaciones.change_justificacion')(MotivoJustificacionUpdate.as_view()),
                            name='motivo_justificacion_edit'
                        ),
                        url(
                            r'^motivos/delete/(?P<pk>[0-9]+)/$', 
                            view=permission_required('justificaciones.change_justificacion')(MotivoJustificacionDelete.as_view()),
                            name='motivo_justificacion_delete'
                        ),

)

