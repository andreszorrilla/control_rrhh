__author__ = 'leonel'
from django.http import HttpResponse
from django.db.models import Q
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from .reports import ReporteFuncionarios, ReporteSolicitud
from apps.configuraciones.models import Funcionario
from apps.vacaciones.models      import Solicitud
from django.views.generic import ListView
from django_sortable.helpers import sortable_helper
import django_filters 
from django.shortcuts import render_to_response

paginate = 10

class Main(TemplateView):
    template_name = 'reportes/main.html'

    def get_context_data(self, **kwargs):
        context = super(Main, self).get_context_data(**kwargs)
        context['url_reporte'] = Funcionario.objects.all() # kwargs.get('reporte') #reverse(kwargs.get('reporte'))

        f = FuncionarioFilter(self.request.GET, queryset=Funcionario.objects.all())
        context['filter'] = f
        #return render_to_response('reportes/main.html', {'filter': f})
        return context

class Funcionarios(TemplateView):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/pdf')
        report = ReporteFuncionarios()
        response.write(report.go())
        return response

        
class Solicitudes(TemplateView):
    template_name = 'reportes/solicitudes.html'

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/pdf')
        solicitud = Solicitud.objects.get(pk=kwargs['pk'])
        report = ReporteSolicitud()
        response.write(report.go(solicitud))
        return response



class FuncionarioFilter(django_filters.FilterSet):
    class Meta:
        model = Funcionario
        fields = {'documento': ['lt', 'gt'],
                  'fecha_ingreso': ['exact'],
                 }

class SolicitudFilter(django_filters.FilterSet):
    class Meta:
        model = Solicitud


def funcionario_list(request):
    f = FuncionarioFilter(request.GET, queryset=Funcionario.objects.all())
    return render_to_response('reportes/main.html', {'filter': f})


def reportes_solicitudes(request):
    return render_to_response('reportes/solicitudes.html', {'filter': []})