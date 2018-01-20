#from django import forms
from apps.helpers.forms import FormHelperHorizontal, FormHelper
from apps.licencias.models import *
from apps.vacaciones.models import *
from crispy_forms.layout import Layout, Field
from crispy_forms.bootstrap import *
import datetime 

from django import forms


class LicenciaForm(forms.ModelForm):
    helper = FormHelperHorizontal()

    cantidad_dias = forms.CharField(label='Cantidad de dias')
    documento = forms.CharField(label='Documento')
    nombre_funcionario = forms.CharField(label='Funcionario')
    id_funcionario = forms.CharField(widget=forms.HiddenInput())
    tipo_motivo = forms.CharField(widget=forms.HiddenInput())
    tipo_documento = forms.CharField(widget=forms.HiddenInput())
    fechas = forms.CharField()
    

    helper.layout = Layout( 
        AppendedText('documento',
                     '<span class="glyphicon glyphicon-search" id="documento_search"></span>',
                     placeholder="Documento",
                     autocomplete="off"),
        Field('id_funcionario', type="hidden"),
        Field('nombre_funcionario', readonly=""),
        FieldWithButtons('motivo', 
                        StrictButton(' <span class="glyphicon glyphicon-plus" aria-hidden="true"></span>',
                            name="go",
                            value="go",
                            css_class="btn btn-small",
                            css_id="new_motivo",
                            title="Nuevo motivo",
                            data_toggle="modal",
                            data_target="#motivoModal"
                        ),
        ),

        Field('cantidad_dias', placeholder="Dias", readonly=""),

        AppendedText('fecha_inicio',
                     '<span class="glyphicon glyphicon-calendar" id="fecha_datepicker"></span>',
                     placeholder="Fecha de inicio",
                     autocomplete="off"
                     ),

        AppendedText('fecha_fin',
                     '<span class="glyphicon glyphicon-calendar" id="fecha_fin_datepicker"></span>',
                     placeholder="Fecha fin",
                     readonly=""),
        Field('tipo_motivo'),
        Field('tipo_documento'),
        AppendedText('fechas',
                    '<span class="glyphicon glyphicon-calendar" id="fechas_datepicker"></span>',
                     placeholder="Fechas",
                     readonly=""
        )
    )

    class Meta:
        model = Licencia


    def __init__(self, *args, **kwargs):
        super(LicenciaForm, self).__init__(*args, **kwargs)
        self.fields['motivo'].queryset = Motivo.objects.all()


    # def clean_fecha_fin(self):
    #     form_data = self.cleaned_data

    #     fecha_inicio = form_data.get('fecha_inicio')
    #     fecha_fin = form_data.get('fecha_fin')


    #     if fecha_inicio > fecha_fin:
    #         raise forms.ValidationError("La fecha de inicio debe ser menor a la fecha final")

    #     return fecha_fin



    def clean(self):
        cleaned_data    = super(LicenciaForm, self).clean()
        cantidad_dias   = cleaned_data.get("cantidad_dias")
        fechas          = cleaned_data.get("fechas")
        fecha_inicio    = cleaned_data.get("fecha_inicio")
        fecha_fin       = cleaned_data.get("fecha_fin")
        motivo          = cleaned_data.get("motivo")
        id_funcionario  = cleaned_data.get("id_funcionario")
        id_user         = cleaned_data.get("id_autor")

        if motivo is None or cantidad_dias is None:
            raise forms.ValidationError({})

        try:
            dias = int(cantidad_dias)

            if dias <= 0:
                raise forms.ValidationError({'cantidad_dias': ["La cantidad de dias debe ser mayor a cero"]})

            fecha_none = fecha_inicio is None or fecha_fin is None
            tipo_motivo = motivo.tipo_motivo

            if tipo_motivo == "corridos":
                if fecha_none:
                    raise forms.ValidationError({'fecha_inicio': ["Este campo es obligatorio."]})
                
                detalles_vacacion = DetalleSolicitud.objects.filter(solicitud__funcionario_id=id_funcionario, fecha__range=(fecha_inicio, fecha_fin), solicitud__estado="procesado")
                if detalles_vacacion:
                    raise forms.ValidationError({'fecha_inicio': ["La fecha ha sido reservada en una solicitud de vacaciones "]})


                detalle_licencia = DetalleLicencia.objects.filter(licencia__funcionario_id=id_funcionario, fecha__range=(fecha_inicio, fecha_fin), licencia__estado="activo")
                if detalle_licencia:
                    raise forms.ValidationError({'fecha_inicio': ["La fecha ha sido reservada en una solicitud de licencia "]})


            else:                
                if fechas is None:
                    raise forms.ValidationError({})

                fechas_str = fechas.split(";")
                if dias != len( fechas_str ):
                    raise forms.ValidationError({'fechas': ["La cantidad de fechas seleccionadas debe ser igual a la cantidad de dias"]})


                #verificacion_fechas_vacaciones(fechas_str, id_funcionario)
                #verificacion_fechas_licencias(fechas_str, id_funcionario)


                for f_str in fechas_str:
                    fecha_date = datetime.datetime.strptime(f_str, "%d/%m/%Y").date()
                    
                    detalles_vacacion = DetalleSolicitud.objects.filter(solicitud__funcionario_id=id_funcionario, fecha=fecha_date, solicitud__estado="procesado")
                    if detalles_vacacion:
                        raise forms.ValidationError({'fechas': ["La fecha " + f_str + " ha sido reservada en una solicitud de vacaciones "]})


                    detalle_licencia = DetalleLicencia.objects.filter(licencia__funcionario_id=id_funcionario, fecha=fecha_date, licencia__estado="activo")
                    if detalle_licencia:
                        raise forms.ValidationError({'fechas': ["La fecha " + f_str + " ha sido reservada en una solicitud de licencia "]})


                    feriados = Feriados.objects.filter(fecha__day=fecha_date.day, fecha__month=fecha_date.month)
                    if feriados:
                        raise forms.ValidationError({'fechas': ["La fecha " + f_str + " coincide con el feriado: " + feriados.first().motivo ]})

        except ValueError:
            raise forms.ValidationError({'cantidad_dias': ["Se debe ingresar un numero."]})


            

class MotivoForm(forms.ModelForm):
    helper = FormHelperHorizontal()

    duracion = forms.IntegerField(label="Cantidad de dias", required=False)

    #dias = forms.CharField(label='Dias')
    #documento = forms.CharField(label='Documento')
    #nombre_funcionario = forms.CharField(label='Funcionario')
    #id_funcionario = forms.CharField(widget=forms.HiddenInput())

    #CHOICES = ((True, 'Si'), (False, 'No'))
    #imputable = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)


    helper.layout = Layout(
        Field('descripcion'),
        #InlineRadios('imputable'),
        Field('tipo_motivo'),
        Field('duracion', min=0),
    )

    class Meta:
        model = Motivo



    def clean(self):
        cleaned_data    = super(MotivoForm, self).clean()
        duracion   = cleaned_data.get("duracion")
        tipo_motivo   = cleaned_data.get("tipo_motivo")

        if duracion is None and tipo_motivo != "permiso":
            raise forms.ValidationError({'duracion': ["Este campo es obligatorio."]})




class FeriadoForm(forms.ModelForm):
    helper = FormHelperHorizontal() 
    fecha = forms.DateField(input_formats=["%d/%m"])

    helper.layout = Layout(
        AppendedText('fecha',
                     '<span class="glyphicon glyphicon-calendar" id="fecha_datepicker"></span>',
                     placeholder="Fecha",
                     autocomplete="off"
                     ),
        Field('motivo'),
    )

    class Meta:
        model = Feriados


    