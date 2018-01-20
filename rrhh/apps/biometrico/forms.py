# -*- coding: utf-8 -*-
from django                         import forms
from apps.biometrico.models         import Transaccion
from apps.helpers.forms             import FormHelperHorizontal, FormHelper
from crispy_forms.layout            import Layout, Field
from crispy_forms.bootstrap         import *
from bootstrap3_datetime.widgets    import DateTimePicker
import datetime
import calendar
from datetime import datetime


class UploadFileForm(forms.Form):
    helper   = FormHelperHorizontal()
    helper.field_class = 'col-md-6'
    file     = forms.FileField(label="Archivo")

    helper.layout = Layout(
        Field('file'),
    )

class TransaccionForm(forms.ModelForm):
    helper   = FormHelperHorizontal()

    blank_choice = [['', '---------'],]


    MONTH_NAMES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    MONTH_CHOICES = blank_choice + [(str(i + 1), MONTH_NAMES[i]) for i in range(0,12)]
    mes = forms.ChoiceField(choices=MONTH_CHOICES)

    YEAR_CHOICES = blank_choice + [(year, year) for year in range(2015, datetime.today().year + 1)][::-1]
    anho = forms.ChoiceField(choices=YEAR_CHOICES, label="Año")

    helper.layout = Layout(
        Field('mes'),
        Field('anho'),
    )

    class Meta:
        model = Transaccion
