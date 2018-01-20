# -*- coding: utf-8 -*-

from apps.biometrico.models         import Marcacion, Transaccion
from apps.configuraciones.models    import Funcionario, Seccion
from apps.vacaciones.models         import DetalleSolicitud, Solicitud
from apps.licencias.models          import Licencia, DetalleLicencia
from django.shortcuts               import render
from django.views.generic           import ListView, DetailView
from django.utils.decorators        import method_decorator
from django.contrib.auth.decorators import login_required
from datetime                       import datetime, timedelta,date, time
from itertools                      import groupby
from django.contrib.auth.models     import Group, User
from apps.justificaciones.models    import Justificacion, MotivoJustificacion
from django.template                import RequestContext
from .forms                         import UploadFileForm, TransaccionForm
from django.http                    import HttpResponseRedirect
from django.core.urlresolvers       import reverse, reverse_lazy

import csv
import sys
import io
from string import strip

from datetime import datetime, date, timedelta
from apps.configuraciones.models import Funcionario, Parametro, Antiguedad, Seccion, Cargo
from apps.vacaciones.models import Periodo
#from dateutil.relativedelta import relativedelta
from datetime import datetime, date
from django.utils import timezone

from apps.biometrico.models import Marcacion, Transaccion
from django.contrib.auth.decorators import user_passes_test




class MarcacionMixin(object):
    model = Marcacion

class MarcacionList(MarcacionMixin, ListView):
    """
        Vista que genera el reporte de las marcaciones.
    """
    template_name = 'biometrico/marcacion_list.html'
    def get_context_data(self, **kwargs):
        context     = super(MarcacionList, self).get_context_data(**kwargs)
        # documento     = self.request.GET['documento'] if 'documento' in self.request.GET else ''
        desde           = get_datetime(self.request.GET['desde'] if 'desde' in self.request.GET else '')
        hasta           = get_datetime(self.request.GET['hasta'] if 'hasta' in self.request.GET else '')
        params_func     = self.request.GET['documento'] if 'documento' in self.request.GET else ''
        params_seccion  = self.request.GET['id_seccion'] if 'id_seccion' in self.request.GET else ''
        user            = self.request.user

        # Si existen funcionarios pendientes
        # Finaliza el programa listando los funcionarios pendientes, es decir,
        # aquellos que estan registrados en el reloj pero no en el sistema.
        funcionarios_pendientes = Funcionario.objects.filter(estado="pendiente")
        if funcionarios_pendientes.count() != 0:
            context["funcionarios_pendientes"]  = funcionarios_pendientes
            context['hay_pendientes']           = funcionarios_pendientes.count() != 0
            return context

        groups = get_groups(self.request.user)

        # Si no existen usuarios pendientes.
        # Y si las fechas 'desde' y 'hasta' son validas.
        if desde and hasta:
            marcaciones_list = []
            filtro_funcionario = {
                                'group__in': groups,
                                'estado': 'activo'
                            }
            if params_func != '':
                filtro_funcionario['documento'] = params_func
            if params_seccion != '':
                filtro_funcionario['seccion_id'] = int(params_seccion)
            funcionarios_list = Funcionario.objects.filter(**filtro_funcionario).order_by('apellido', 'seccion_id')
            marcaciones_funcionario = []
            for funcionario in funcionarios_list:
                marcaciones_list = []
                for n in range(1 + int((hasta - desde).days)):
                    current_date = (desde + timedelta(n)).date()
                    filtro_marcacion = {
                                'fecha_hora__range': (  datetime.combine(current_date, time.min),
                                                        datetime.combine(current_date, time.max)),
                                'funcionario': funcionario
                            } 

                    marcaciones = Marcacion.objects.filter(**filtro_marcacion).order_by('fecha_hora')
                    week_days = {"Sun": "Dom", "Mon": "Lun", "Tue": "Mar", "Wed": "Mie", "Thu": "Jue", "Fri": "Vie", "Sat": "Sab"}
                    day     =   week_days[current_date.strftime("%a")]
                    fecha_str = current_date.strftime("%d/%m/%Y - " + day)
                    
                    fecha_vacacion_descripcion = get_vacacion_licencia_descripcion(current_date, funcionario)

                    fechas_justificaciones = get_justificacion_marcacion_descripcion(current_date, funcionario)

                    marcaciones_list.append([fecha_str, marcaciones, fecha_vacacion_descripcion, fechas_justificaciones])
                marcaciones_funcionario.append([marcaciones_list, funcionario])

            context["marcaciones_funcionarios_list"] = marcaciones_funcionario
            context["hora_emision"] = datetime.today().strftime("%d/%m/%Y %H:%M")
            context["cantidad_funcionarios"] = funcionarios_list.count()
            context["autor"] = user
            context["group"] = user.groups.first()
        context["secciones"] = Seccion.objects.filter(group__in=groups)
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MarcacionList, self).dispatch(*args, **kwargs)




class ObtenerMarcaciones(ListView):
    template_name = 'configuraciones/buscador.html'

    def get_queryset(self):
        return None


def get_datetime(str):
    try:
        return datetime.strptime(str, "%d/%m/%Y")
    except(ValueError):
        return None


def extract_date(marcacion):
    'extracts the starting date from an entity'
    return marcacion.fecha_hora.date()


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


def get_groups(user):
    groups = []
    if user.is_superuser:
        groups = Group.objects.all().values_list('id', flat=True)
    else:
        groups = user.groups.values_list('id', flat=True)
    return groups

def get_vacacion_licencia_descripcion(current_date, funcionario):
    detalle = DetalleSolicitud.objects.filter(
                                    fecha=current_date,
                                    solicitud__funcionario=funcionario,
                                    solicitud__estado="procesado"
                                ).first()
    if not detalle is None:
        return "s/ Sol. Vac. " + str(detalle.solicitud.id)
    licencia = Licencia.exist_by_fecha(current_date, funcionario)
    if not licencia is None:
        return "s/ Sol. Lic. " + str(licencia.id)

    return ""


def get_justificacion_marcacion_descripcion(current_date, funcionario):
    filtro_marcacion = {
                                'fecha_hora__range': (  datetime.combine(current_date, time.min),
                                                        datetime.combine(current_date, time.max)),
                                'funcionario': funcionario,
                                'estado': 'activo'
                            } 
    justificaciones = Justificacion.objects.filter(**filtro_marcacion)
    
    text_list = []
    for justificacion in justificaciones:
        hora    = justificacion.fecha_hora
        numero  = str(justificacion.get_numero())
        tipo    = str(justificacion.tipo_justificacion).upper()
        text_list.append([hora, "s/ Just. %s Nº %s \n" % (tipo, numero)])
    return text_list



def is_int(value):
    try:
        int(value)
        return True
    except:
        return False

def to_datetime(fecha_hora):
    return datetime.strptime(fecha_hora, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc, second=0, microsecond=0)

def convertir(archivo, transaccion):
    csv_file     = archivo
    decoded_file = csv_file.read().decode('utf-8')
    io_string    = io.StringIO(decoded_file)

    funcionarios_set = set()

    transaccion.save()
    mes  = transaccion.mes
    anho = transaccion.anho

    hoy  = datetime.now()

    for row in csv.reader(io_string, delimiter='\t'):
        row = map(strip, row)
        if len(row) == 0 or len(row) != 6:
            continue
        elif not is_int(row[0]):
            continue
        else:
            cedula  = row[0]
            fecha   = row[1]
            fecha_hora = to_datetime(fecha)

            if fecha_hora.year == anho and fecha_hora.month == mes:
                funcionario = Funcionario.get_funcionario_actual_por_documento(cedula)
                repetido = Marcacion.objects.filter(funcionario=funcionario, fecha_hora=fecha_hora).count() > 0
                if not repetido:
                    marcacion = Marcacion(transaccion=transaccion, funcionario=funcionario, fecha_hora=fecha_hora)
                    marcacion.save()



@user_passes_test(lambda u: u.is_superuser)
def carga_marcaciones(request):
    if request.method == 'POST':
        uploadFileForm  = UploadFileForm(request.POST, request.FILES)
        transaccionForm = TransaccionForm(request.POST)
        if uploadFileForm.is_valid() and transaccionForm.is_valid():
            transaccion = transaccionForm.save(commit=False)
            convertir(request.FILES['file'], transaccion)
            return HttpResponseRedirect(reverse_lazy("carga_marcaciones"))
    else:
        uploadFileForm = UploadFileForm()
        transaccionForm = TransaccionForm()
    return render(request, 'biometrico/carga_marcaciones.html', {'uploadFileForm': uploadFileForm, 'transaccionForm': transaccionForm})

