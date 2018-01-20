# -*- encoding: utf-8 -*-
from crispy_forms.bootstrap import AppendedText
from crispy_forms.layout import Layout, Field
from datetime import date
from django.db.models import Q, Sum
from django.forms.models import inlineformset_factory
from django import forms
from apps.configuraciones.models import Parametro
from .models import Solicitud, DetalleSolicitud, Periodo
from apps.licencias.models import DetalleLicencia, Feriados
from apps.helpers.forms import FormHelperHorizontal
import datetime
from apps.configuraciones.models import Antiguedad

max_dias = 30
min_dias = 0


class SolicitudForm(forms.Form):
    numero = forms.CharField()
    documento = forms.CharField(label='Documento')
    dias = forms.CharField(label='Días')
    id_id_funcionario = forms.IntegerField(widget=forms.HiddenInput())
    funcionario = forms.CharField(label='Funcionario')
    dias_restantes = forms.CharField(label='Días Restantes', required=False)
    fecha = forms.DateField(label='Fecha de solicitud')
    dias = forms.CharField()
    cantidad_de_dias = forms.IntegerField()
    helper = FormHelperHorizontal()

    helper.layout = Layout(
        Field('numero', value=Solicitud.objects.count() + 1, readonly=''),
        AppendedText('documento', '<span class="glyphicon glyphicon-search" id="buscar_documento"></span>',
                     placeholder="Nº Documento", ),
        Field('id_id_funcionario'),
        Field('funcionario', placeholder="Funcionario", readonly=""),
        Field('dias_restantes', placeholder="Días Restantes", readonly=""),
        AppendedText('fecha', '<span class="glyphicon glyphicon-calendar" id="fecha_datepicker"></span>',
                     placeholder="Fecha", ),
        AppendedText('dias', '<span class="glyphicon glyphicon-calendar" id="dias_datepicker"></span>',
                     placeholder="Días", readonly=""),
        Field('cantidad_de_dias', placeholder="Cantidad de Días", readonly=""),
    )
    class Meta:
        model = Solicitud

    #Verifica que la cantidad de dias solicitados no supere los disponibles
    def clean_cantidad_de_dias(self):
        form_data = self.cleaned_data
        cantidad_dias = form_data.get('cantidad_de_dias')
        documento = form_data.get('documento')

        periodos = Periodo.objects.filter(Q(funcionario__documento=documento)).order_by('anho')

        dias_disponibles = periodos.aggregate(Sum('libres'))['libres__sum']

        if periodos.count() == 0:
            dias_disponibles = 0

        if cantidad_dias > dias_disponibles:
            raise forms.ValidationError("La cantidad de días disponibles es menor a la solicitada")

        return cantidad_dias


    def clean(self):
        cleaned_data    = super(SolicitudForm, self).clean()
        dias            = cleaned_data.get("dias")
        id_funcionario  = cleaned_data.get("id_id_funcionario")

        if dias is None or id_funcionario is None:
            return


        fechas_str = dias.split(";")


        for f_str in fechas_str:
            fecha_date = datetime.datetime.strptime(f_str, "%d/%m/%Y").date()
            
            detalles_vacacion = DetalleSolicitud.objects.filter(solicitud__funcionario_id=id_funcionario, fecha=fecha_date, solicitud__estado="procesado")
            if detalles_vacacion:
                raise forms.ValidationError({'dias': ["La fecha " + f_str + " ha sido reservada en una solicitud de vacaciones "]})


            detalle_licencia = DetalleLicencia.objects.filter(licencia__funcionario_id=id_funcionario, fecha=fecha_date, licencia__estado="activo")
            if detalle_licencia:
                raise forms.ValidationError({'dias': ["La fecha " + f_str + " ha sido reservada en una solicitud de licencia "]})

            feriados = Feriados.objects.filter(fecha__day=fecha_date.day, fecha__month=fecha_date.month)
            if feriados:
                raise forms.ValidationError({'dias': ["La fecha " + f_str + " coincide con el feriado: " + feriados.first().motivo ]})


class DetalleSolicitudForm(forms.ModelForm):
    class Meta:
        model = DetalleSolicitud


SolicitudDetalleFormSet = inlineformset_factory(Solicitud, DetalleSolicitud)


class AjustesDetailCreate(forms.Form):

    id_funcionario = forms.Field()
    funcionario = forms.CharField()
    anho = forms.IntegerField(label='Año', min_value=date.today().year-2, max_value=date.today().year)
    libres = forms.IntegerField(label='Días Libres', min_value=min_dias, max_value=max_dias)
    helper = FormHelperHorizontal()
    helper.layout = Layout(
        Field('id_funcionario', type="hidden"),
        Field('funcionario', readonly=""),
        Field('anho', placeholder="Año"),
        Field('libres', placeholder="Días Libres", readonly="")
    )

    def clean(self):
        cleaned_data    = super(AjustesDetailCreate, self).clean()
        anho           = cleaned_data.get("anho")
        id_funcionario  = cleaned_data.get("id_funcionario")
        libres = cleaned_data.get("libres")

        periodos = Periodo.objects.filter(funcionario_id=id_funcionario, anho=anho)
        
        if periodos.count() > 0:
            raise forms.ValidationError({"anho": "El periodo " + str(anho) + " ya se encuentra creado para el funcionario"})

        if anho is None:
            return


        try:
            antiguedad = Antiguedad.objects.filter(anhos_antiguedad__lte=anho).order_by('-anhos_antiguedad')[:1].get()
            
            if antiguedad.dias_libres < libres :
                raise forms.ValidationError({"libres": "La antiguedad del funcionario correspondiente al " + str(anho) + " es hasta " + str(antiguedad.dias_libres) + " dias"})
        except Antiguedad.DoesNotExist, e:
            raise forms.ValidationError({"libres": "El funcionario no puede solicitar vacaciones porque no tiene antiguedad suficiente"})
        

    def cantidad_anhos_desde(fecha_desde):
        before = datetime.strptime(fecha_desde, '%d/%m/%Y')
        now = datetime.now()
        type(now - before)
        return (now - before).days / 365
        




class AjustesDetailUpdate(forms.Form):
    id_periodo = forms.Field()
    funcionario = forms.CharField()
    anho = forms.IntegerField(label='Año')
    total = forms.IntegerField(label='Total', min_value=min_dias, max_value=max_dias)
    libres = forms.IntegerField(label='Días Libres', min_value=min_dias, max_value=max_dias)
    helper = FormHelperHorizontal()
    helper.layout = Layout(
        Field('id_periodo', type="hidden"),
        Field('funcionario', readonly=""),
        Field('anho', readonly=""),
        Field('total', placeholder="Total"),
        Field('libres', placeholder="Días Libres")
    )

    def clean_libres(self):
        form_data = self.cleaned_data
        total = form_data.get('total')
        libres = form_data.get('libres')
        if total < libres:
            raise forms.ValidationError("La cantidad de días libres no puede ser mayor al total del periodo")
        return libres