from crispy_forms.bootstrap import *
from crispy_forms.layout import Layout, Field
from django import forms
from django.contrib.auth.models import Group
from .models import Justificacion, MotivoJustificacion
from apps.configuraciones.models    import Funcionario
from crispy_forms.helper import FormHelper
from apps.helpers.forms import FormHelperHorizontal
from bootstrap3_datetime.widgets import DateTimePicker




class JustificacionForm(forms.ModelForm):
    use_required_attribute = False

    numero                          = forms.CharField()
    documento                       = forms.CharField(label='Documento')
    funcionario                     = forms.Field(widget=forms.HiddenInput())
    funcionario_nombre_completo     = forms.CharField(label='Funcionario')
    fecha_hora                      = forms.DateTimeField(
                                        widget=DateTimePicker(
                                            options={
                                                        "format": "DD/MM/YYYY HH:mm",
                                                        "pickSeconds": True,
                                                        "icons": {
                                                            "time": "glyphicon glyphicon-time",
                                                            "date": "glyphicon glyphicon-calendar",
                                                            "up": "glyphicon glyphicon-arrow-up",
                                                            "down": "glyphicon glyphicon-arrow-down"
                                                        }
                                                    }
                                        ),
                                        label='Fecha y Hora',
                                    )
    observaciones   = forms.Field(widget=forms.Textarea, required=False)

    helper = FormHelperHorizontal()

    numero_f = '%04d' % (Justificacion.objects.count() + 1)

    helper.layout = Layout(
        Field('numero', value=numero_f, readonly=''),
        AppendedText('documento', '<span class="glyphicon glyphicon-search" id="buscar_documento"></span>',
                     placeholder="N Documento", autocomplete="off", autofocus="on"),
        Field('funcionario'),
        Field('funcionario_nombre_completo', placeholder="Funcionario", readonly=""),
        Field('tipo_justificacion'),
        Field('tipo_marcacion'),
        Field('fecha_hora', placeholder="dd/mm/aaaa HH:MM", autocomplete="off"),
    )
    class Meta:
        model = Justificacion
        fields = ['tipo_marcacion', 'fecha_hora', 'tipo_justificacion', 'motivo_justificacion', 'observaciones']




class MotivoJustificacionForm(forms.ModelForm):
    use_required_attribute = False
    helper = FormHelperHorizontal()
    
    class Meta:
        model = MotivoJustificacion
        fields = ['descripcion']