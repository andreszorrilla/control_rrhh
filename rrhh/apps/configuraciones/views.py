# -*- encoding: utf-8 -*-
from django.core.paginator import Paginator

from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, FormView, TemplateView
from .models import Antiguedad, Funcionario, Parametro, Cargo, Seccion
from .forms import AntiguedadForm, FuncionarioForm, ParametroForm, CargoForm, SeccionForm
from django.core.urlresolvers import reverse_lazy
from django_sortable.helpers import sortable_helper
from django.conf import global_settings
import json
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import permission_required

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


#nro de elementos para paginar
paginate = 20

class AntiguedadMixin(object):
	model = Antiguedad

class AntiguedadCreate(AntiguedadMixin, CreateView):
	form_class = AntiguedadForm

class AntiguedadList(AntiguedadMixin, ListView):
	context_object_name = "antiguedades"
	paginate_by = paginate

	def get_queryset(self):
		user = self.request.user
		queryset = super(AntiguedadList, self).get_queryset()
		return sortable_helper(self.request, queryset)

class AntiguedadDetail(AntiguedadMixin, DetailView):
	pass

class AntiguedadUpdate(AntiguedadMixin, UpdateView):
	form_class = AntiguedadForm





class CargoMixin(object):
	model = Cargo



class FuncionarioMixin(object):
	model = Funcionario


class FuncionarioList(FuncionarioMixin, ListView):
	context_object_name = "funcionarios"

	def get_context_data(self, **kwargs):
		context = super(FuncionarioList, self).get_context_data(**kwargs)

		estado = self.request.GET['estado'] if 'estado' in self.request.GET else ''
		filtro = self.request.GET['filtro'] if 'filtro' in self.request.GET else ''
		
		groups = []
		if self.request.user.is_superuser:
			groups = Group.objects.all().values_list('id', flat=True)
		else:
			groups = self.request.user.groups.values_list('id', flat=True)

		if estado != '':
			funcionarios_list = Funcionario.objects.filter(Q(estado=estado, nombre__icontains=filtro, 		group__in=groups)
													  | Q(estado=estado, apellido__icontains=filtro, 	group__in=groups)
													  | Q(estado=estado, documento__icontains=filtro, 	group__in=groups)) \
													.order_by("-id")

		else:
			funcionarios_list = Funcionario.objects.filter(Q(nombre__icontains=filtro, 		group__in=groups)
													  | Q(apellido__icontains=filtro, 	group__in=groups)
													  | Q(documento__icontains=filtro, 	group__in=groups)) \
													.order_by("-id")

		funcionarios_list = sortable_helper(self.request, funcionarios_list)



		funcionarios_list 	= sortable_helper(self.request, funcionarios_list)
		paginator 			= Paginator(funcionarios_list, paginate)

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


class FuncionarioCreate(FuncionarioMixin, CreateView):
	form_class = FuncionarioForm

	# Basado en:
	# http://stackoverflow.com/questions/24041649/filtering-a-model-in-a-createview-with-get-queryset
	def get_form_kwargs(self):
		kwargs = super(FuncionarioCreate, self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs



class FuncionarioDetail(FuncionarioMixin, DetailView):
	pass


class FuncionarioUpdate(FuncionarioMixin, UpdateView):
	form_class = FuncionarioForm

	# Basado en:
	# http://stackoverflow.com/questions/24041649/filtering-a-model-in-a-createview-with-get-queryset
	def get_form_kwargs(self):
		kwargs = super(FuncionarioUpdate, self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs


class FuncionarioUpdateEstado(TemplateView):
	def get(self, request, *args, **kwargs):
		id_funcionario = self.kwargs['pk']
		funcionario = Funcionario.objects.get(id=id_funcionario)
		funcionario.estado = 'inactivo' if funcionario.estado == 'activo' else 'activo'
		funcionario.save()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Vistas para Parametros
class ParametroMixin(object):
	model = Parametro


class ParametroDetail(ParametroMixin, DetailView):
	def get_context_data(self, **kwargs):
		context = super(ParametroDetail, self).get_context_data(**kwargs)
		return context


class ParametroUpdate(ParametroMixin, UpdateView):
	form_class = ParametroForm




#######################
###### SECCIONES ######
#######################

class SeccionMixin(object):
	model = Seccion


class SeccionList(SeccionMixin, ListView):
	context_object_name = "secciones"
	template_name = 'configuraciones/seccion_list.html'

	def get_context_data(self, **kwargs):

		context = super(SeccionList, self).get_context_data(**kwargs)
		filtro = self.request.GET['filtro'] if 'filtro' in self.request.GET else ''


		groups = []
		if self.request.user.is_superuser:
			groups = Group.objects.all().values_list('id', flat=True)
		else:
			groups = self.request.user.groups.values_list('id', flat=True)


		secciones_list = Seccion.objects.filter(Q(nombre__icontains=filtro, group__in=groups)).order_by("-id")
		secciones_list = sortable_helper(self.request, secciones_list)


		secciones_list 	= sortable_helper(self.request, secciones_list)
		paginator 		= 	 Paginator(secciones_list, paginate)

		try:
			page = int(self.request.GET.get('page', '1'))
		except:
			page = 1

		try:
			secciones = paginator.page(page)
		except(EmptyPage, InvalidPage):
			secciones = paginator.page(1)
		index 		=	secciones.number - 1  
		max_index 	=	len(paginator.page_range)
		start_index =	index - 3 if index >= 3 else 0
		end_index 	=	index + 3 if index <= max_index - 3 else max_index
		page_range 	=	paginator.page_range[start_index:end_index]

		context['secciones'] = secciones
		context['page_range'] = page_range

		return context



class SeccionCreate(SeccionMixin, CreateView):
	form_class = SeccionForm

	def get_form_kwargs(self):
		kwargs = super(SeccionCreate, self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs


class SeccionUpdate(SeccionMixin, UpdateView):
	form_class = SeccionForm

	def get_form_kwargs(self):
		kwargs = super(SeccionUpdate, self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs


class SeccionDetail(SeccionMixin, DetailView):
	pass


class SeccionDelete(SeccionMixin, DeleteView):
	pass



#######################
####### CARGOS ########
#######################

class CargoMixin(object):
	model = Cargo

class CargoList(CargoMixin, ListView):
	context_object_name = "cargos"

	def get_context_data(self, **kwargs):
		context = super(CargoList, self).get_context_data(**kwargs)

		groups = []
		if self.request.user.is_superuser:
			groups = Group.objects.all().values_list('id', flat=True)
		else:
			groups = self.request.user.groups.values_list('id', flat=True)


		filtro = self.request.GET['filtro'] if 'filtro' in self.request.GET else ''
		cargos_list = Cargo.objects.filter(Q(nombre__icontains=filtro, seccion__group__in=groups)).order_by("-id")
		cargos_list = sortable_helper(self.request, cargos_list)

		paginator = Paginator(cargos_list, paginate)
		try:
			page = int(self.request.GET.get('page', '1'))
		except:
			page = 1

		try:
			cargos = paginator.page(page)
		except(EmptyPage, InvalidPage):
			cargos = paginator.page(1)
		index = cargos.number - 1  
		max_index = len(paginator.page_range)
		start_index = index - 3 if index >= 3 else 0
		end_index = index + 3 if index <= max_index - 3 else max_index
		page_range = paginator.page_range[start_index:end_index]

		context['cargos'] = cargos
		context['page_range'] = page_range

		return context


class CargoCreate(CargoMixin, CreateView):
	form_class = CargoForm
	def get_form_kwargs(self):
		kwargs = super(CargoCreate, self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs


class CargoUpdate(CargoMixin, UpdateView):
	form_class = CargoForm
	def get_form_kwargs(self):
		kwargs = super(CargoUpdate, self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

class CargoDetail(CargoMixin, DetailView):
	pass

class CargoDelete(CargoMixin, DeleteView):
	pass

class JSONCargosBySeccion(TemplateView):
	def get(self, request, *args, **kwargs):
		data = None
		id_seccion = kwargs.get("id_seccion")
		cargos = Cargo.objects.filter(seccion_id=id_seccion)
		data = serializers.serialize("json", cargos, fields=("id", "nombre"))
		return HttpResponse(data, content_type="application/json; charset=utf-8")

# Buscar
class Buscador(ListView):
	template_name = 'configuraciones/buscador.html'

	def get_queryset(self):
		return None


