from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.views.generic import TemplateView

from django.contrib.auth.decorators import login_required


admin.autodiscover()



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'RRHH.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #Admin
    url(
        r'^admin/',
        include(admin.site.urls)
    ),

    #Media
    url(
        r'^media/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root':  settings.MEDIA_ROOT, }
    ),

    url(r'^rrhh/', 
        login_required( TemplateView.as_view(template_name='base.html') ), 
        name="base_url"
    ),

    url(r'^$',
        TemplateView.as_view(template_name="configuraciones/buscador.html"),
        name="searcher_url"
    ),



    #Configuraciones
    url(
        r'^configuraciones/',
        include('apps.configuraciones.urls')
    ),

    #Vacaciones
    url(
        r'^vacaciones/',
        include('apps.vacaciones.urls')
    ),

    #Reportes
    url(
        r'^reportes/',
        include('apps.reportes.urls')
    ),

    #Licencias
    url(
        r'^licencias/',
        include('apps.licencias.urls')
    ),

    # Biometrico
    url(
        r'^biometrico/',
        include('apps.biometrico.urls')
    ),

    # Justificaciones
    url(
        r'^justificaciones/',
        include('apps.justificaciones.urls')
    ),

    # Login
    url(r'^login/$', 'django.contrib.auth.views.login'),

    # Logout
    url(r'^logout/$', 'django.contrib.auth.views.logout'),


    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html'}),



)

