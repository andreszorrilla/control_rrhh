__author__ = 'lgamarra'
from .models import Periodo, Solicitud, DetalleSolicitud
from django.contrib import admin


admin.site.register(Periodo)
admin.site.register(Solicitud)
admin.site.register(DetalleSolicitud)
