# -*- encoding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from apps.configuraciones.models import Funcionario
from django.contrib.auth.models import User
from datetime import datetime

class Transaccion(models.Model):
    mes         = models.IntegerField()
    anho        = models.IntegerField()
    # autor      = models.ForeignKey(User, default=2)
    created_at  = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at  = models.DateTimeField(auto_now=True, blank=True)

    def __unicode__(self):
        return str(self.mes) + "/" + str(self.anho)


class Marcacion(models.Model):
    funcionario = models.ForeignKey(Funcionario)
    transaccion = models.ForeignKey(Transaccion)
    fecha_hora	= models.DateTimeField()
    created_at 	= models.DateTimeField(auto_now_add=True, blank=True)
    updated_at 	= models.DateTimeField(auto_now=True, blank=True)

    OPCIONES = (
        ('activo', 'Aactivo'),
        ('inactivo', 'Inactivo'),
    )
    estado = models.CharField('Estado', choices=OPCIONES, default='activo', max_length=9)

    def __unicode__(self):
        return self.funcionario.nombre + ' ' + str(self.fecha_hora)


    def get_fecha(self):
        return self.fecha_hora.strftime('%d/%m/%Y - %a').encode('utf-8')

    def get_hora(self):
        return self.fecha_hora.strftime('%H:%M').encode('utf-8')

    def get_id_transaccion(self):
        return 

    class Meta:
        verbose_name_plural = 'Marcaciones'


class Marcacion(models.Model):
    funcionario = models.ForeignKey(Funcionario)
    transaccion = models.ForeignKey(Transaccion)
    fecha_hora  = models.DateTimeField()
    created_at  = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at  = models.DateTimeField(auto_now=True, blank=True)

    OPCIONES = (
        ('activo', 'Aactivo'),
        ('inactivo', 'Inactivo'),
    )
    estado = models.CharField('Estado', choices=OPCIONES, default='activo', max_length=9)

    def __unicode__(self):
        return self.funcionario.nombre + ' ' + str(self.fecha_hora)


    def get_fecha(self):
        return self.fecha_hora.strftime('%d/%m/%Y - %a').encode('utf-8')

    def get_hora(self):
        return self.fecha_hora.strftime('%H:%M').encode('utf-8')

    def get_id_transaccion(self):
        return

    class Meta:
        verbose_name_plural = 'Marcaciones'
