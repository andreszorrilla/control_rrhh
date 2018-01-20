from django.core.urlresolvers       import reverse, reverse_lazy
from django.shortcuts               import render
from django.views.generic           import ListView, DetailView
from django.utils.decorators        import method_decorator
from django.contrib.auth.decorators import login_required
from datetime                       import datetime, timedelta,date, time
from itertools                      import groupby
from django.contrib.auth.models     import Group, User
from django.views.generic           import CreateView, ListView, FormView, DetailView, UpdateView, DeleteView, TemplateView, View
from apps.justificaciones.models    import Justificacion, MotivoJustificacion
from apps.configuraciones.models    import Funcionario
from .forms                         import JustificacionForm, MotivoJustificacionForm
from django.http                    import Http404, HttpResponseRedirect
from django.contrib                 import messages
from django.db                      import transaction

from django.db.models import Q, Sum, F

from django_sortable.helpers import sortable_helper
from django.core.paginator import Paginator


paginate = 20

class JustificacionMixin(object):
    model = Justificacion

class JustificacionList(JustificacionMixin, ListView):
    """
        Vista que genera el reporte de las justificaciones.
    """
    template_name = 'justificaciones/justificacion_list.html'
    def get_context_data(self, **kwargs):
        context     = super(JustificacionList, self).get_context_data(**kwargs)
        context['justificaciones'] = Justificacion.objects.all()
        return context

    def get_context_data(self, **kwargs):
        context = super(JustificacionList, self).get_context_data(**kwargs)

        estado = self.request.GET['estado'] if 'estado' in self.request.GET else ''
        filtro = self.request.GET['filtro'] if 'filtro' in self.request.GET else ''
        user   = self.request.user
        


        if estado != '':
            filtro = {    Q(estado=estado,  funcionario__nombre__icontains=filtro )
                        | Q(estado=estado,   funcionario__apellido__icontains=filtro )
                        | Q(estado=estado,   funcionario__documento__icontains=filtro )  }
            

        else:
            filtro = {    Q(funcionario__nombre__icontains=filtro )
                        | Q(funcionario__apellido__icontains=filtro )
                        | Q(funcionario__documento__icontains=filtro )  }
            
        justificacion_list = Justificacion.objects.filter(*filtro).order_by("-id")


        justificacion_list = sortable_helper(self.request, justificacion_list)

        paginator = Paginator(justificacion_list, paginate)
        try:
            page = int(self.request.GET.get('page', '1'))
        except:
            page = 1

        try:
            justificaciones = paginator.page(page)
        except(EmptyPage, InvalidPage):
            justificaciones = paginator.page(1)
        index       = justificaciones.number - 1
        max_index   = len(paginator.page_range)
        start_index = index - 3 if index >= 3 else 0
        end_index   = index + 3 if index <= max_index - 3 else max_index
        page_range  = paginator.page_range[start_index:end_index]


        context['justificaciones']  = justificaciones
        context['page_range']       = page_range
        context["autor"] = user
        context["group"] = user.groups.first()

        return context






    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(JustificacionList, self).dispatch(*args, **kwargs)


class JustificacionCreate(JustificacionMixin, CreateView):
    form_class = JustificacionForm
    template_name = 'justificaciones/justificacion_form.html'

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        template_name = 'justificaciones/justificacion_form.html'
        form = self.form_class(request.POST)

        if form.is_valid():
            justificacion = form.save(commit=False)            
            pk = form.cleaned_data['funcionario']
            justificacion.funcionario = Funcionario.objects.get(pk=pk.decode('utf-8'))
            justificacion.autor       = request.user
            justificacion.save()
            return HttpResponseRedirect(reverse_lazy("justificaciones_list") + "?estado=activo")

        return render(request, template_name, {'form': form})




class JustificacionUpdate(JustificacionMixin, UpdateView):
    form_class = JustificacionForm


class JustificacionDetail(JustificacionMixin, DetailView):
    def get_context_data(self, **kwargs):
        context = super(JustificacionDetail, self).get_context_data(**kwargs)
        context['justificacion'] = Justificacion.objects.get(pk=context['justificacion'].id)

        user                = self.request.user
        context['autor']    = context['justificacion'].autor

        groups = []
        if user.is_superuser:
            context['group']    = Group.objects.first()  # Default: Departamento de RRHH
        else:
            context['group']    = user.groups.first()

        return context


class JustificacionDelete(JustificacionMixin, DeleteView):
    model = Justificacion
    #success_url = reverse_lazy('motivo-list')

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        licencia = Justificacion.objects.get(pk=pk)
        licencia.estado = "inactivo"
        licencia.save()

        return HttpResponseRedirect(reverse_lazy("justificaciones_list") + "?estado=activo")




# Motivos de Justificaciones

class MotivoJustificacionMixin(object):
    model = MotivoJustificacion

class MotivoJustificacionList(MotivoJustificacionMixin, ListView):
    """
        Vista que genera el reporte de las motivos_justificaciones.
    """
    template_name = 'justificaciones/motivo_justificacion_list.html'
    def get_context_data(self, **kwargs):
        context     = super(MotivoJustificacionList, self).get_context_data(**kwargs)
        context['motivos_justificaciones'] = MotivoJustificacion.objects.all()
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MotivoJustificacionList, self).dispatch(*args, **kwargs)


class MotivoJustificacionCreate(MotivoJustificacionMixin, CreateView):
    form_class      = MotivoJustificacionForm
    template_name   = 'justificaciones/motivo_justificacion_new.html'
    success_url     = reverse_lazy('motivos_justificaciones_list')


class MotivoJustificacionUpdate(MotivoJustificacionMixin, UpdateView):
    form_class      = MotivoJustificacionForm
    template_name   = 'justificaciones/motivo_justificacion_edit.html'
    success_url     = reverse_lazy('motivos_justificaciones_list')


class MotivoJustificacionDetail(MotivoJustificacionMixin, DetailView):
    template_name   = 'justificaciones/motivo_justificacion_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(MotivoJustificacionDetail, self).get_context_data(**kwargs)
        context['motivo_justificacion'] = MotivoJustificacion.objects.get(pk=context['object'].id)
        return context


class MotivoJustificacionDelete(MotivoJustificacionMixin, DeleteView):
    success_url     = reverse_lazy('motivos_justificaciones_list')
    success_message = "El motivo fue eliminado correctamente."

    def delete(self, request, *args, **kwargs):
        return super(MotivoJustificacionDelete, self).delete(request, *args, **kwargs)