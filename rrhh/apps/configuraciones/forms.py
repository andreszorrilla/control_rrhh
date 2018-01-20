# -*- encoding: utf-8 -*-
from crispy_forms.bootstrap import *
from crispy_forms.layout import Layout, Field
from django import forms
from apps.helpers.forms import FormHelperHorizontal
from models import Antiguedad, Funcionario, Parametro, Cargo, Seccion
from django.contrib.auth.models import Group




class AntiguedadForm(forms.ModelForm):
    helper = FormHelperHorizontal()
    helper.layout = Layout(
        Field('anhos_antiguedad',   placeholder="Años de Antiguedad"),
        Field('dias_libres',        placeholder="Días Libres"),
    )

    class Meta:
        model = Antiguedad

class CargoForm(forms.ModelForm):
    helper = FormHelperHorizontal()

    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-7'

    helper.layout = Layout(
        Field('seccion'),
        Field('nombre', placeholder="Nombre")
    )
    class Meta:
        model = Cargo

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(CargoForm, self).__init__(*args, **kwargs)

        # Lista para campo seccion
        groups = []
        if user.is_superuser:
            groups = Group.objects.all().values_list('id', flat=True)
        else:
            groups = user.groups.values_list('id', flat=True)
        secciones = Seccion.objects.filter(group__in=groups)

        self.fields['seccion'].queryset = secciones


class SeccionForm(forms.ModelForm):
    helper = FormHelperHorizontal()

    helper.layout = Layout(
        Field('group', "Grupo"),
        Field('nombre', placeholder="Nombre")
    )
    class Meta:
        model = Seccion

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(SeccionForm, self).__init__(*args, **kwargs)

        # Labels
        self.fields['group'].label = "Grupo"

        # Lista para campo grupo
        groups = []
        if user.is_superuser:
            groups = Group.objects.all()
        else:
            groups = user.groups

        self.fields['group'].queryset = groups






class FuncionarioForm(forms.ModelForm):
    helper = FormHelperHorizontal()
    
    helper.layout = Layout(
        Field('nombre'),
        Field('apellido'),
        Field('documento'),
        AppendedText('fecha_ingreso',
                     '<span class="glyphicon glyphicon-calendar" id="fecha_ingreso_datepicker"></span>'),
        Field('group'),
        FieldWithButtons('seccion', 
                        StrictButton(' <span class="glyphicon glyphicon-plus" aria-hidden="true"></span>',
                            name="go",
                            value="go",
                            css_class="btn btn-small",
                            title="Nueva seccion",
                            data_toggle="tooltip"
                        ),
        ),
        FieldWithButtons('cargo', 
                        StrictButton(' <span class="glyphicon glyphicon-plus" aria-hidden="true"></span>',
                            name="go",
                            value="go",
                            css_class="btn btn-small",
                            css_id="new_cargo",
                            title="Nuevo cargo",
                            data_toggle="tooltip"
                        ),
        ),
        AppendedText('fecha_nacimiento',
                     '<span class="glyphicon glyphicon-calendar" id="fecha_nacimiento_datepicker"></span>'),
        Field('email', placeholder="ejemplo@dominio.com"),
        Field('estado'),
    )

    class Meta:
        model = Funcionario

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(FuncionarioForm, self).__init__(*args, **kwargs)


        # Labels
        self.fields['group'].label = "Grupo"

        # Listas para selects
        self.fields['cargo'].queryset = Cargo.objects.all()

        groups = []
        if user.is_superuser:
            groups = Group.objects.all()
        else:
            groups = user.groups

        self.fields['group'].queryset = groups

        groups = groups.values_list('id', flat=True)
        secciones = Seccion.objects.filter(group__in=groups)

        self.fields['seccion'].queryset = secciones


class ParametroForm(forms.ModelForm):
    helper = FormHelperHorizontal()
    helper.layout = Layout(
        Field('institucion', placeholder="Institución"),
        Field('anhos_acumulables_vacaciones', placeholder="Años Acumulables de Vacaciones"),
        Field('logo', placeholder="Logo"),
    )

    class Meta:
        model = Parametro



