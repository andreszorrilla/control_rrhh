# -*- encoding: utf-8 -*-
from django.core.paginator import Paginator
from django.views.generic import CreateView, ListView, FormView, DetailView, UpdateView, DeleteView, TemplateView, View
from django.core.urlresolvers import reverse_lazy, reverse
from .models import Periodo, Solicitud, DetalleSolicitud
from apps.configuraciones.models import Funcionario, Parametro, Antiguedad
from .forms import SolicitudForm, AjustesDetailCreate, AjustesDetailUpdate
from django.http import HttpResponse
from django.db.models import Q, Sum, F
from datetime import date
from django.core import serializers
from django.http import HttpResponseRedirect
from datetime import datetime
import json
from django.db import transaction, connection
from django_sortable.helpers import sortable_helper
from dateutil.relativedelta import relativedelta


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Group, User


#nro de elementos para paginar
paginate = 20

class PeriodoMixin(object):
	model = Periodo

class PeriodoList(PeriodoMixin, ListView):
	paginate_by = paginate
	context_object_name = "periodos"


	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(PeriodoList, self).dispatch(*args, **kwargs)


class SolicitudMixin(object):
	model = Solicitud


class SolicitudCreate(FormView):
	template_name = 'vacaciones/solicitud_form.html'
	form_class = SolicitudForm
	success_url = reverse_lazy("solicitud_list")

	@transaction.atomic
	def post(self, request, *args, **kwargs):

		form_class 	= self.get_form_class()
		form 		= self.get_form(form_class)

		if not form.is_valid():
			return self.form_invalid(form)

		numero 			= self.request.POST['numero']
		id_funcionario 	= self.request.POST['id_id_funcionario']
		fecha 			= self.request.POST['fecha']
		fecha 			= datetime.strptime(fecha, "%d/%m/%Y").date()
		cantidad_dias 	= self.request.POST['cantidad_de_dias']
		dias 			= self.request.POST['dias']

		dias = dias.split(';')

		#guarda la solicitud

		solicitud = Solicitud.objects.create(funcionario_id=id_funcionario, fecha=fecha, cantidad_dias=cantidad_dias, estado='procesado', autor=request.user)

		periodos = Periodo.objects.filter(funcionario_id=id_funcionario, estado='activo').order_by('anho')

		#carga el detalle de las vacaciones segun el periodo
		dias_pos = 0
		dias_a_cargar = int(cantidad_dias)
		for periodo in periodos:
			if dias_a_cargar > 0:
				dias_libres = periodo.libres
				if dias_libres >= dias_a_cargar:
					for i in range(dias_a_cargar):
						DetalleSolicitud.objects.create(solicitud_id=solicitud.id, periodo_id=periodo.id,
														fecha=datetime.strptime(dias[dias_pos], "%d/%m/%Y").date())
						dias_pos += 1
						dias_a_cargar -= 1
						periodo.usados = F('usados') + 1
						periodo.libres = F('libres') - 1
						periodo.save()

				else:
					for j in range(dias_libres):
						DetalleSolicitud.objects.create(solicitud_id=solicitud.id, periodo_id=periodo.id,
														fecha=datetime.strptime(dias[dias_pos], "%d/%m/%Y").date())
						dias_pos += 1
						dias_a_cargar -= 1
						periodo.usados = F('usados') + 1
						periodo.libres = F('libres') - 1
						periodo.save()
			else:
				break

		return HttpResponseRedirect(reverse_lazy("solicitud_list") + "?estado=procesado")


	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(SolicitudCreate, self).dispatch(*args, **kwargs)


class SolicitudAnular(TemplateView):
	@transaction.atomic
	def get(self, request, *args, **kwargs):
		id_solicitud = self.kwargs['pk']
		solicitud = Solicitud.objects.get(id=id_solicitud)
		if solicitud.estado != 'anulado':
			solicitud.estado = 'anulado'
			solicitud.save()
			detalles = DetalleSolicitud.objects.filter(solicitud_id=id_solicitud)

			for detalle in detalles:
				periodo = Periodo.objects.get(id=detalle.periodo_id)
				periodo.usados = F('usados') - 1
				periodo.libres = F('libres') + 1
				periodo.save()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class SolicitudList(SolicitudMixin, ListView):
	template_name = 'vacaciones/solicitud_list.html'


	def get_context_data(self, **kwargs):
		context = super(SolicitudList, self).get_context_data(**kwargs)

		estado = self.request.GET['estado'] if 'estado' in self.request.GET else ''
		filtro = self.request.GET['filtro'] if 'filtro' in self.request.GET else ''
		
		# Listado de grupos para restriccion
		groups = []
		if self.request.user.is_superuser:
			groups = Group.objects.all().values_list('id', flat=True)
		else:
			groups = self.request.user.groups.values_list('id', flat=True)

		if estado != '':
			solicitud_list = Solicitud.objects.filter(Q(estado=estado, 	funcionario__nombre__icontains=filtro, 		funcionario__group__in=groups )
												   | Q(estado=estado, 	funcionario__apellido__icontains=filtro, 	funcionario__group__in=groups )
												   | Q(estado=estado, 	funcionario__documento__icontains=filtro, 	funcionario__group__in=groups )) \
				.order_by("-id")

		else:
			solicitud_list = Solicitud.objects.filter(Q(funcionario__nombre__icontains=filtro, 			funcionario__group__in=groups )
												   | Q(funcionario__apellido__icontains=filtro, 		funcionario__group__in=groups )
												   | Q(funcionario__documento__icontains=filtro, 	funcionario__group__in=groups )) \
				.order_by("-id")



		solicitud_list = sortable_helper(self.request, solicitud_list)

		paginator = Paginator(solicitud_list, paginate)
		try:
			page = int(self.request.GET.get('page', '1'))
		except:
			page = 1

		try:
			solicitudes = paginator.page(page)
		except(EmptyPage, InvalidPage):
			solicitudes = paginator.page(1)
		index = solicitudes.number - 1
		max_index = len(paginator.page_range)
		start_index = index - 3 if index >= 3 else 0
		end_index = index + 3 if index <= max_index - 3 else max_index
		page_range = paginator.page_range[start_index:end_index]

		context['solicitudes'] = solicitudes
		context['page_range'] = page_range

		return context

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(SolicitudList, self).dispatch(*args, **kwargs)


class SolicitudDetail(SolicitudMixin, DetailView):
	def get_context_data(self, **kwargs):
		context = super(SolicitudDetail, self).get_context_data(**kwargs)

		user 				= self.request.user
		context['fechas'] 	= DetalleSolicitud.get_fechas(context['solicitud'].id)
		total_libres 		= Periodo.objects.filter(funcionario_id=context['solicitud'].funcionario_id, estado="activo").aggregate(total_libres=Sum('libres'))
		context["libres"] 	= total_libres['total_libres'] if total_libres['total_libres'] else 0
		context['autor']	= context['solicitud'].autor

		groups = []
		if user.is_superuser:
			context['group']	= Group.objects.first()  # Default: Departamento de RRHH
		else:
			context['group']	= user.groups.first()

		

		return context


	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(SolicitudDetail, self).dispatch(*args, **kwargs)


class JSONSolicitudBuscarFuncionario(TemplateView):
	def get(self, request, *args, **kwargs):
		documento = request.GET['documento']


		groups = []
		if self.request.user.is_superuser:
			groups = Group.objects.all().values_list('id', flat=True)
		else:
			groups = self.request.user.groups.values_list('id', flat=True)



		funcionarios = Funcionario.objects.filter(documento=documento, estado='activo', group__in=groups)

		if funcionarios.count() == 0:
			return HttpResponse(None, content_type="application/json; charset=utf-8")

		periodos = Periodo.objects.filter(funcionario__documento=documento, estado='activo').aggregate(
			total_libres=Sum('libres'))
		total_libres = periodos['total_libres'] if periodos['total_libres'] else 0

		json_funcionarios = serializers.serialize("json", funcionarios)

		data = json.dumps({'funcionario': json.loads(json_funcionarios)[0], 'total_libres': total_libres})

		return HttpResponse(data, content_type="application/json; charset=utf-8")





 ## Ajustes

class AjustesMixin(object):
	model = Funcionario



class AjustesList(AjustesMixin, ListView):
	template_name = 'vacaciones/ajustes_list.html'	
	context_object_name = "funcionarios"

	def get_context_data(self, **kwargs):
		context = super(AjustesList, self).get_context_data(**kwargs)
		filtro = self.request.GET['filtro'] if 'filtro' in self.request.GET else ''
		groups = []
		if self.request.user.is_superuser:
			groups = Group.objects.all().values_list('id', flat=True)
		else:
			groups = self.request.user.groups.values_list('id', flat=True)
		funcionarios_list = Funcionario.objects.filter(	Q(estado='activo', nombre__icontains=filtro,		group__in=groups )
												  | Q(estado='activo', apellido__icontains=filtro,	group__in=groups )
												  | Q(estado='activo', documento__icontains=filtro,	group__in=groups ))
		funcionarios_list = sortable_helper(self.request, funcionarios_list)
		for funcionario in funcionarios_list:
			periodos = Periodo.objects.filter(funcionario_id=funcionario.id, estado='activo').aggregate(total_libres=Sum('libres'))
			total_libres = periodos['total_libres'] if periodos['total_libres'] else 0
			funcionario.total_libres = total_libres

		paginator = Paginator(funcionarios_list, paginate)
		try:
			page = int(self.request.GET.get('page', '1'))
		except:
			page = 1

		try:
			funcionarios = paginator.page(page)
		except(EmptyPage, InvalidPage):
			funcionarios = paginator.page(1)

		index = funcionarios.number - 1  
		max_index = len(paginator.page_range)
		start_index = index - 3 if index >= 3 else 0
		end_index = index + 3 if index <= max_index - 3 else max_index
		page_range = paginator.page_range[start_index:end_index]
		
		context['funcionarios'] = funcionarios
		context['page_range'] = page_range
		return context


	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(AjustesList, self).dispatch(*args, **kwargs)


class AjustesDetail(DetailView):
	model = Funcionario
	template_name = 'vacaciones/ajustes_detail.html'

	def get_context_data(self, **kwargs):
		context = super(AjustesDetail, self).get_context_data(**kwargs)
		periodos = Periodo.objects.filter(funcionario_id=context['funcionario'].id).order_by('-anho')
		context['periodos'] = periodos

		return context


	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(AjustesDetail, self).dispatch(*args, **kwargs)


class AjustesDetailCreate(FormView):
	form_class = AjustesDetailCreate
	template_name = 'vacaciones/ajustes_detail_create.html'

	def get_initial(self):
		id_funcionario = self.request.GET['id_funcionario']
		funcionario = Funcionario.objects.get(id=id_funcionario)
		return {'id_funcionario': id_funcionario, 'funcionario': funcionario.nombre + " " + funcionario.apellido, 'id_libres': 50}

	def post(self, request, *args, **kwargs):

		form_class = self.get_form_class()
		form = self.get_form(form_class)
		
		id_funcionario = self.request.POST['id_funcionario']
		anho = self.request.POST['anho']
		libres = self.request.POST['libres']

		if not form.is_valid():
			return self.form_invalid(form)

		Periodo.objects.create(anho=anho, total=libres, usados=0, libres=libres, funcionario_id=id_funcionario)

		return HttpResponseRedirect(reverse("ajustes_vacaciones_detail", args=[id_funcionario]))


	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(AjustesDetailCreate, self).dispatch(*args, **kwargs)


class AjustesDetailUpdate(FormView):
	form_class = AjustesDetailUpdate
	template_name = 'vacaciones/ajustes_detail_update.html'
	periodo = None

	def get_initial(self):
		id_periodo = self.kwargs['pk']
		periodo = Periodo.objects.get(id=id_periodo)
		self.periodo = periodo
		return {'id_periodo': id_periodo,
				'funcionario': periodo.funcionario.nombre + " " + periodo.funcionario.apellido,
				'anho': periodo.anho,
				'total': periodo.total,
				'libres': periodo.libres}

	def get_context_data(self, **kwargs):
		context = super(AjustesDetailUpdate, self).get_context_data(**kwargs)
		context['funcionario'] = self.periodo.funcionario
		return context


	@transaction.atomic
	def form_valid(self, form):
		id_periodo = self.request.POST['id_periodo']
		total = self.request.POST['total']
		libres = self.request.POST['libres']
		usados = int(total) - int(libres)

		periodo = Periodo.objects.get(id=id_periodo)

		periodo.total = total
		periodo.libres = libres
		periodo.usados = usados

		periodo.save()

		return HttpResponseRedirect(reverse("ajustes_vacaciones_detail", args=[periodo.funcionario.id]))


	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(AjustesDetailUpdate, self).dispatch(*args, **kwargs)



class JSONObtenerCantidadDias(TemplateView):
	def get(self, request, *args, **kwargs):
		

		id_funcionario = request.GET['id_funcionario']
		anho = request.GET['anho']

		data = json.dumps({})


		funcionario = Funcionario.objects.get(pk=id_funcionario)
		fecha_ingreso = funcionario.fecha_ingreso


		# Obtener fechas del periodo anterior y la de hoy
		fecha_periodo_anterior = date(int(anho), fecha_ingreso.month, fecha_ingreso.day)
		fecha_hoy              = date.today()


		#min_year = date.today().year - 1
		#max_year = date.today().year - 2
		#if not ( min_year >= int(anho) and max_year <= int(anho) ):
		#	data = json.dumps({"result": "failed", "message": "You messed up"})
		#	return HttpResponse(data, content_type="application/json; charset=utf-8")

		valid = False
		for i in range(3):
			fecha_periodo = fecha_ingreso.replace(year = fecha_hoy.year - i)
			if fecha_periodo <= fecha_hoy and fecha_periodo == fecha_periodo_anterior:
				valid = True
				break
		if not valid:
			data = json.dumps({"result": "failed", "message": "You messed up"})
			return HttpResponse(data, content_type="application/json; charset=utf-8")


		if fecha_periodo_anterior < fecha_ingreso:
			data = json.dumps({"result": "failed", "message": "You messed up"})
			return HttpResponse(data, content_type="application/json; charset=utf-8")


		# Verificar si se puede usar periodo actual
		dif_anhos_periodo_hoy = abs( relativedelta(fecha_periodo_anterior, fecha_hoy).years )
		if dif_anhos_periodo_hoy < 0: 
			return data

	   # Si se puede, entonces obtener anhos
		anhos_antiguedad = abs( relativedelta(fecha_ingreso, fecha_periodo_anterior).years )
		
		if fecha_ingreso >= fecha_periodo_anterior:
			anhos_antiguedad = abs( relativedelta(datetime.now(), fecha_periodo_anterior).years )

		antiguedad = Antiguedad.objects.filter(anhos_antiguedad__lte=anhos_antiguedad).order_by("-anhos_antiguedad").first()
		if antiguedad:
			data = json.dumps({'cantidad_dias': antiguedad.dias_libres})

		return HttpResponse(data, content_type="application/json; charset=utf-8")




class JSONFuncionarioPorCelula(TemplateView):    
	def get(self, request, *args, **kwargs):
		cedula = kwargs.get("cedula")
		funcionarios = Funcionario.objects.filter(documento=cedula)

		funcionario = funcionarios[0]

		periodos = Periodo.objects.filter(funcionario_id=funcionario.id, estado="activo").order_by('-anho')
		
		periodos_list 	= {}
		fecha_periodos 	= {}

		for periodo in periodos:
			detalle					  	= DetalleSolicitud.objects.filter(solicitud__estado="procesado", solicitud__funcionario_id=funcionario.id, periodo_id=periodo.id, fecha__gt=date(2015, 11, 1))
			detalle_json 				= serializers.serialize("json", detalle, fields=("fecha"))
			periodos_list[periodo.anho] = detalle_json
			
			fi = funcionario.fecha_ingreso
			fecha_periodos[periodo.anho] = [ fi.replace(year=periodo.anho).strftime('%b %Y'), fi.replace(year=periodo.anho + 1).strftime('%b %Y') ]


		periodos = serializers.serialize("json", periodos, fields=("id", "anho", "usados", "libres"))
		data = json.dumps({'nombre': funcionario.nombre, 'apellido': funcionario.apellido, 'dias_libres': 0, 'periodos': periodos, 'fechas': periodos_list, 'fechas_periodos': fecha_periodos })
		return HttpResponse(data, content_type="application/json; charset=utf-8")




#######Consultas

class ConsultaList(ListView):
	template_name = 'vacaciones/consulta_list.html'
	paginate_by = paginate
	context_object_name = "funcionarios"

	def get_queryset(self):
		filtro = self.request.GET['filtro'] if 'filtro' in self.request.GET else ''
		funcionarios = Funcionario.objects.filter(Q(estado='activo', nombre__icontains=filtro)
												  | Q(estado='activo', apellido__icontains=filtro)
												  | Q(estado='activo', documento__icontains=filtro))
		funcionarios = sortable_helper(self.request, funcionarios)
		for funcionario in funcionarios:
			periodos = Periodo.objects.filter(funcionario_id=funcionario.id, estado='activo').aggregate(
				total_libres=Sum('libres'))
			total_libres = periodos['total_libres'] if periodos['total_libres'] else 0
			funcionario.total_libres = total_libres

		return funcionarios


	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(ConsultaList, self).dispatch(*args, **kwargs)