from django.shortcuts import render
from apps.licencias.models import *
from django.core.urlresolvers import reverse_lazy, reverse
from django.core import serializers
from django.views.generic import CreateView, ListView, FormView, DetailView, UpdateView, DeleteView, TemplateView, View
from django.utils import timezone
import json
from apps.licencias.forms import LicenciaForm, MotivoForm, FeriadoForm
from django.http import HttpResponse, JsonResponse
from django.db import transaction, connection
from django.http import HttpResponseRedirect
from datetime import date 
import time
import datetime
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse_lazy
from django_sortable.helpers import sortable_helper
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Group, User
from django.core.paginator import Paginator

paginate = 20

class LicenciaMixin(object):
	model = Licencia

# Create your views here.

class LicenciaListView(LicenciaMixin, ListView):
	context_object_name = "licencias"

	def get_context_data(self, **kwargs):
		context = super(LicenciaListView, self).get_context_data(**kwargs)		
		estado = self.request.GET['estado'] if 'estado' in self.request.GET else ''
		filtro = self.request.GET['filtro'] if 'filtro' in self.request.GET else ''

		groups = []
		if self.request.user.is_superuser:
			groups = Group.objects.all().values_list('id', flat=True)
		else:
			groups = self.request.user.groups.values_list('id', flat=True)

		if estado != '':
			licencias_list = Licencia.objects.filter(	 Q(estado=estado, funcionario__nombre__icontains=filtro,		funcionario__group__in=groups )
														| Q(estado=estado, funcionario__apellido__icontains=filtro,		funcionario__group__in=groups )
														| Q(estado=estado, funcionario__documento__icontains=filtro,	funcionario__group__in=groups )) \
				.order_by("-id")

		else:
			licencias_list = Licencia.objects.filter(	 Q(funcionario__nombre__icontains=filtro,		funcionario__group__in=groups )
														| Q(funcionario__apellido__icontains=filtro,		funcionario__group__in=groups )
														| Q(funcionario__documento__icontains=filtro,		funcionario__group__in=groups )) \
				.order_by("-id")
		licencias_list = sortable_helper(self.request, licencias_list)



		paginator = Paginator(licencias_list, paginate)
		try:
			page = int(self.request.GET.get('page', '1'))
		except:
			page = 1

		try:
			licencias = paginator.page(page)
		except(EmptyPage, InvalidPage):
			licencias = paginator.page(1)
		index = licencias.number - 1  
		max_index = len(paginator.page_range)
		start_index = index - 3 if index >= 3 else 0
		end_index = index + 3 if index <= max_index - 3 else max_index
		page_range = paginator.page_range[start_index:end_index]

		context['licencias'] = licencias
		context['page_range'] = page_range

		return context

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(LicenciaListView, self).dispatch(*args, **kwargs)




class LicenciaCreate(FormView):
	template_name = 'licencias/licencia_form.html'
	form_class = LicenciaForm
	success_url = reverse_lazy("licencia_list")

	def get(self, request, *args, **kwargs):
		motivo_form = MotivoForm
		return render_to_response(self.template_name, {'form': self.form_class, 'motivo_form': motivo_form}, context_instance=RequestContext(request))


	def post(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)

		form.errors.pop('fecha_solicitud')
		form.errors.pop('estado')
		form.errors.pop('funcionario')
		form.errors.pop('tipo_motivo')
		form.errors.pop('autor')
		#form.errors.pop('tipo_documento')
		
		motivo = request.POST.get('motivo')

		if motivo == '':
			form.errors.pop('fechas')
			form.errors.pop('fecha_inicio')
			form.errors.pop('fecha_fin')

			return self.form_invalid(form)



		tipo_motivo = Motivo.objects.get(pk=motivo).tipo_motivo

		if tipo_motivo == "corridos":
			form.errors.pop("fechas")
		else:
			form.errors.pop("fecha_inicio")
			form.errors.pop("fecha_fin")

			fechas = self.request.POST['fechas'].split(";")

			self.request.POST['fecha_i']	= fechas[0]
			self.request.POST['fecha_f']	= fechas[-1]

		if not form.is_valid():
			return self.form_invalid(form)

		
		return self.form_valid(form)


	@transaction.atomic
	def form_invalid(self, form):
		response = super(LicenciaCreate, self).form_invalid(form)

		for error in form.errors:
			print error

		if self.request.is_ajax():
			return JsonResponse(form.errors, status=400)
		else:
			return response


	@transaction.atomic
	def form_valid(self, form):
		id_funcionario	= self.request.POST['id_funcionario']
		motivo			= self.request.POST['motivo']
		fecha_inicio	= ''
		fecha_fin		= ''


		if self.request.POST['fecha_inicio'] == '' or self.request.POST['fecha_fin'] == '':
			fecha_inicio = self.request.POST['fecha_i']
			fecha_fin 	 = self.request.POST['fecha_f']
		else:
			fecha_inicio = self.request.POST['fecha_inicio']
			fecha_fin 	 = self.request.POST['fecha_fin']


		cantidad_dias = self.request.POST['cantidad_dias']

		fecha_inicio = datetime.datetime.strptime(fecha_inicio, "%d/%m/%Y").date()
		fecha_fin = datetime.datetime.strptime(fecha_fin, "%d/%m/%Y").date()



		licencia = Licencia(cantidad_dias=int(cantidad_dias) ,funcionario_id=int(id_funcionario), motivo_id=int(motivo), fecha_solicitud=date.today(), fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, autor=self.request.user)
		licencia.save()


		if self.request.POST.get('fecha_i') != None:
			fechas = self.request.POST['fechas'].split(";")
			for f in fechas:
				fecha = datetime.datetime.strptime(f, "%d/%m/%Y").date()
				detalle = DetalleLicencia(fecha=fecha, licencia_id=licencia.id)
				detalle.save()

		return HttpResponseRedirect(reverse_lazy("licencia_list") + "?estado=activo")

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(LicenciaCreate, self).dispatch(*args, **kwargs)



class LicenciaDetail(LicenciaMixin, DetailView):
	def get_context_data(self, **kwargs):
		context = super(LicenciaDetail, self).get_context_data(**kwargs)
		context['licencia'] = Licencia.objects.get(pk=context['licencia'].id)
		context['fechas'] 	= DetalleLicencia.get_fechas(context['licencia'].id)
		user 				= self.request.user
		context['autor']	= context['licencia'].autor

		groups = []
		if user.is_superuser:
			context['group']	= Group.objects.first()  # Default: Departamento de RRHH
		else:
			context['group']	= user.groups.first()

		return context

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(LicenciaDetail, self).dispatch(*args, **kwargs)


class MotivoAjaxCreate(FormView):
	def post(self, request, *args, **kwargs):
		#motivo = Motivo(request.POST)
		#print motivo.save()

		motivo = Motivo(descripcion=request.POST['descripcion'], duracion=int(request.POST['duracion']), tipo_motivo=request.POST['tipo_motivo'])
		motivo.save()
		
		data = serializers.serialize('json', Motivo.objects.all())
		return HttpResponse(data, content_type="application/json; charset=utf-8")


class CreateFechaFinalLicencia(TemplateView):
	def get(self, request, *args, **kwargs):
		
		fecha_inicio = request.GET['fecha']
		dias = int(request.GET['dias'])
		tipo_motivo = request.GET['tipo_motivo']

		fecha_inicial = datetime.datetime.strptime(fecha_inicio, "%d/%m/%Y").date()
		fecha = datetime.datetime.strptime(fecha_inicio, "%d/%m/%Y").date()
		

		son_dias_habiles = tipo_motivo == "habiles"

		while dias > 0:
			fecha += datetime.timedelta(days=1)
			weekday = fecha.weekday()
			if son_dias_habiles and weekday >= 5: # sunday = 6
				continue
			dias -= 1

		if son_dias_habiles:
			feriados = Feriados.objects.filter( fecha__range=(fecha_inicial, fecha) )
			fecha += datetime.timedelta( days=feriados.count() )
		data = json.dumps({'fecha_fin': fecha.strftime("%d/%m/%Y") })
		print data
		return HttpResponse(data, content_type="application/json; charset=utf-8")

		
		

class JSONObtenerMotivo(TemplateView):
	def get(self, request, *args, **kwargs):
		id_motivo = request.GET['id_motivo']
		data = None

		motivo = Motivo.objects.get(pk=id_motivo)
		data = json.dumps({'cantidad_dias': motivo.duracion, "imputable": motivo.imputable, "tipo_motivo": motivo.tipo_motivo})

		return HttpResponse(data, content_type="application/json; charset=utf-8")



class LicenciaDeleteView(DeleteView):
	model = Licencia
	#success_url = reverse_lazy('motivo-list')

	def get(self, request, *args, **kwargs):
		pk = kwargs['pk']
		licencia = Licencia.objects.get(pk=pk)

		licencia.estado = "inactivo"

		licencia.save()

		#licencia.delete()
		return HttpResponseRedirect(reverse_lazy("licencia_list") + "?estado=activo")


	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(LicenciaDeleteView, self).dispatch(*args, **kwargs)


###################################
########### MOTIVOS ###############
###################################

class MotivoListView(ListView):
	model = Motivo
	def get_context_data(self, **kwargs):
		context = super(MotivoListView, self).get_context_data(**kwargs)

		motivos_list = Motivo.objects.all()
		motivos_list = sortable_helper(self.request, motivos_list)
		motivos_list = sortable_helper(self.request, motivos_list)

		paginator = Paginator(motivos_list, paginate)
		try:
			page = int(self.request.GET.get('page', '1'))
		except:
			page = 1

		try:
			motivos = paginator.page(page)
		except(EmptyPage, InvalidPage):
			motivos = paginator.page(1)
		index = motivos.number - 1  
		max_index = len(paginator.page_range)
		start_index = index - 3 if index >= 3 else 0
		end_index = index + 3 if index <= max_index - 3 else max_index
		page_range = paginator.page_range[start_index:end_index]

		context['motivos'] = motivos
		context['page_range'] = page_range

		return context

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(MotivoListView, self).dispatch(*args, **kwargs)


class MotivoViewForm(FormView):
	template_name = 'licencias/motivo_form.html'
	form_class = MotivoForm()
	success_url = reverse_lazy("motivo_list")

	def get(self, request, *args, **kwargs):
		pk = kwargs.get("pk")
		if pk == None:
			return render_to_response(self.template_name, {'form': self.form_class}, context_instance=RequestContext(request))
		else:
			template_name = "licencias/motivo_edit.html"
			motivo = get_object_or_404(Motivo, pk=pk)
			form_class = MotivoForm(instance=motivo)
			return render_to_response(template_name, {'form': form_class}, context_instance=RequestContext(request))

	def post(self, request, *args, **kwargs):
			
		form_class = MotivoForm
		form = self.get_form(form_class)
		
		if not form.is_valid():
			return self.form_invalid(form)
		cantidad_dias = request.POST.get("duracion", "0")


		print kwargs


		m = Motivo(id=kwargs.get("pk"), descripcion=request.POST['descripcion'], duracion=cantidad_dias, tipo_motivo=request.POST['tipo_motivo'])
		m.save()

		return self.form_valid(form)


	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(MotivoViewForm, self).dispatch(*args, **kwargs)


class MotivoDeleteView(DeleteView):
	model = Motivo
	success_url = reverse_lazy('motivo-list')

	def get(self, request, *args, **kwargs):
		id_motivo = kwargs['pk']
		motivo = Motivo.objects.get(pk=id_motivo)

		motivo.delete()
		return HttpResponseRedirect(reverse_lazy("motivo_list"))


	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(MotivoDeleteView, self).dispatch(*args, **kwargs)


###################################
########## FERIADOS ###############
###################################


##########   	##########   	#########   	#########   	   ##	   		#####	  		#########
##				##			  	##	   ##   	   ###	  	  	 ## ##	 		##   ##			##	   ##
#######		 	#######	  		#######	 	   	   ###	  	 	##   ##			##	   ##   	##	   ##
##			 	##				##   ##	 	  	   ###	  		########		##   ##   		##	   ##
##			 	#########		##	   ##   	#########      ##	  ##   		#####   		#########

class FeriadoListView(ListView):
	model = Feriados
	def get_context_data(self, **kwargs):
		context = super(FeriadoListView, self).get_context_data(**kwargs)
		context['feriados'] = Feriados.objects.all()
		return context



	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(FeriadoListView, self).dispatch(*args, **kwargs)



class FeriadoViewForm(FormView):
	template_name = 'licencias/feriado_form.html'
	form_class = FeriadoForm
	success_url = reverse_lazy("feriado_list")


	def get(self, request, *args, **kwargs):
		pk = kwargs.get("pk")
		if pk == None:
			return render_to_response(self.template_name, {'form': self.form_class}, context_instance=RequestContext(request))
		else:
			template_name = "licencias/feriado_form.html"
			feriado = get_object_or_404(Feriados, pk=pk)
			kkkkk = datetime.datetime.strftime(feriado.fecha, "%d/%m")
			form_class = FeriadoForm(instance=feriado, initial={'fecha': kkkkk})
			return render_to_response(template_name, {'form': form_class}, context_instance=RequestContext(request))



	def post(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)

		if not form.is_valid():
			return self.form_invalid(form)


		pk = kwargs.get("pk")
		arg_fecha = request.POST.get('fecha')
		motivo 	  = request.POST.get('motivo')


		fecha = datetime.datetime.strptime(arg_fecha, "%d/%m").date()
		feriado = Feriados(id=pk, motivo=motivo, fecha=fecha )
		feriado.save()
		
		return self.form_valid(form)



	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(FeriadoViewForm, self).dispatch(*args, **kwargs)


class FeriadoMixin(object):
	model = Feriados

class FeriadoDetail(FeriadoMixin, DetailView):
	def get_context_data(self, **kwargs):
		context = super(FeriadoDetail, self).get_context_data(**kwargs)
		context['feriados'] = Feriados.objects.get(pk=context['feriados'].id)
		return context


	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(FeriadoDetail, self).dispatch(*args, **kwargs)


class FeriadoDeleteView(DeleteView):
	model = Feriados
	success_url = reverse_lazy('feriados-list')

	def get(self, request, *args, **kwargs):
		id_feriado = kwargs['pk']
		feriado = Feriados.objects.get(pk=id_feriado)

		feriado.delete()
		return HttpResponseRedirect(reverse_lazy("feriado_list"))


	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(FeriadoDeleteView, self).dispatch(*args, **kwargs)



class JSONFeriados(TemplateView):
	def get(self, request, *args, **kwargs):
		data = serializers.serialize("json", Feriados.objects.all())
		return HttpResponse(data, content_type="application/json; charset=utf-8")
