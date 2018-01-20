# -*- encoding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group
from datetime import datetime, date

class Antiguedad(models.Model):
    anhos_antiguedad = models.IntegerField('Años de Antiguedad', unique=True,
                                           error_messages={'unique': 'Ya existe una Antiguedad con'
                                                                     'este Año de Antiguedad.'})
    dias_libres = models.IntegerField("Días Libres", )

    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        verbose_name = 'Antiguedad'
        verbose_name_plural = 'Antiguedades'

    def __unicode__(self):
        return str(self.anhos_antiguedad) + ' | ' + str(self.dias_libres)

    def get_absolute_url(self):
        return reverse("antiguedad_detail", args=[self.pk])

    def get_update_url(self):
        return reverse("antiguedad_update", args=[self.pk])

    def get_delete_url(self):
        return reverse("antiguedad_delete", args=[self.pk])

    @models.permalink
    def get_success_url(self):
        return reverse('antiguedad_list')


class Seccion(models.Model):
    nombre =   models.CharField(max_length=45)
    group  =   models.ForeignKey(Group, default=1)

    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __unicode__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('seccion_list')

    def get_update_url(self):
        return reverse("seccion_update", args=[self.pk])

    def get_delete_url(self):
        return reverse('seccion_list')

    @models.permalink
    def get_success_url(self):
        return reverse('seccion_list')

    def id_str(self):
        return str(self.id)


class Cargo(models.Model):
    nombre = models.CharField(max_length=45)
    seccion = models.ForeignKey(Seccion)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __unicode__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('cargo_list')

    def get_update_url(self):
        return reverse("cargo_update", args=[self.pk])

    def get_delete_url(self):
        return reverse('cargo_list')

    @models.permalink
    def get_success_url(self):
        return reverse('cargo_list')


class Funcionario(models.Model):
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    documento = models.CharField(max_length=45, db_index=True, unique=True)
    fecha_ingreso = models.DateField('Fecha de Ingreso')
    fecha_nacimiento = models.DateField('Fecha de Nacimiento', blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    OPCIONES = (
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('pendiente', 'Pendiente'),
    )
    estado = models.CharField('Estado', choices=OPCIONES, default='activo', max_length=9)
    cargo   = models.ForeignKey(Cargo)
    seccion = models.ForeignKey(Seccion)
    group = models.ForeignKey(Group, default=1)

    def __unicode__(self):
        return self.nombre + ' ' + self.apellido

    @models.permalink
    def get_absolute_url(self):
        return 'funcionario_detail', [str(self.id)]

    def get_nombre_completo(self):
        return self.nombre + ' ' + self.apellido


    @staticmethod
    def get_funcionario_actual_por_documento(documento):
        funcionario = Funcionario.objects.filter(estado='activo', documento=documento).first()
        # Si no hay funcionarios activos
        if not funcionario:
            funcionario = Funcionario.objects.filter(documento=documento).first()
            # Si no hay funcionarios (pendientes o inactivos)
            if not funcionario:
                seccion = Seccion.objects.get_or_create(nombre="--- Seccion No Especificada ---")[0]
                cargo   = Cargo.objects.get_or_create(nombre="--- Cargo No Especificado ---", seccion_id=seccion.id)[0]
                funcionario = Funcionario( nombre='', apellido='', documento=documento, estado='pendiente', seccion_id=seccion.id, cargo_id=cargo.id, fecha_ingreso=date.today() )
                funcionario.save()
        return funcionario



class Parametro(models.Model):
    institucion = models.CharField(max_length=45)
    anhos_acumulables_vacaciones = models.IntegerField()
    logo = models.ImageField(upload_to='archivos/')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    @models.permalink
    def get_absolute_url(self):
        return 'parametro_detail', [str(self.id)]