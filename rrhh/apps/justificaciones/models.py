# -*- coding: utf-8 -*-
from django.db import models

from django.core.urlresolvers import reverse
from apps.configuraciones.models import Funcionario
from django.contrib.auth.models import User
from datetime import datetime

class MotivoJustificacion(models.Model):
    descripcion = models.CharField(max_length=30, blank=False, unique=True)
    
    def __unicode__(self):
        return self.descripcion

    def can_be_deleted(self):
        return not Justificacion.objects.filter(motivo_justificacion_id=self.id).exists()

class Justificacion(models.Model):
    OPCIONES_TIPO_MARCACION = (
        ('e', 'Entrada'),
        ('s', 'Salida'),
    )
    OPCIONES_TIPO_JUSTICACION = (
        ('fdh', 'Marcación fuera del horario'),
        ('om',  'Omisión de Marcación'),
    )
    funcionario 		= models.ForeignKey(Funcionario)
    fecha_hora  		= models.DateTimeField()
    tipo_marcacion 		= models.CharField('Tipo Marcacion', choices=OPCIONES_TIPO_MARCACION, max_length=1)
    tipo_justificacion 	= models.CharField('Tipo Justificacion', choices=OPCIONES_TIPO_JUSTICACION, max_length=3)
    motivo_justificacion= models.ForeignKey(MotivoJustificacion, on_delete=models.PROTECT, blank=True, null=True)
    observaciones 		= models.CharField(max_length=50)
    autor				= models.ForeignKey(User)
    created_at  		= models.DateTimeField(auto_now_add=True, blank=True)
    updated_at  		= models.DateTimeField(auto_now=True, blank=True)

    OPCIONES = (
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    )
    estado = models.CharField('Estado', choices=OPCIONES, default='activo', max_length=9)

    def get_numero(self):
        return '%04d' % self.id

