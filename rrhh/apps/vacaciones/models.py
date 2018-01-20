# -*- encoding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from apps.configuraciones.models import Funcionario
from django.contrib.auth.models import User
import locale

class Periodo(models.Model):
    anho = models.IntegerField('Año', max_length=4)
    total = models.IntegerField()
    usados = models.IntegerField()
    libres = models.IntegerField()
    OPCIONES = (
        ('activo', 'Activo'),
        ('vencido', 'Vencido'),
    )
    estado = models.CharField('Estado', choices=OPCIONES, default='activo', max_length=8)
    funcionario = models.ForeignKey(Funcionario)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __unicode__(self):
        return self.funcionario.nombre + ' ' + str(self.anho) 

    def get_anhos_periodos(self):
        return str(self.anho) + " - " + str(self.anho + 1)

class Solicitud(models.Model):
    numero =        models.IntegerField('Numero de solicitud', null=True)
    fecha_emision = models.DateField(auto_now=True)
    funcionario =   models.ForeignKey(Funcionario)
    fecha =         models.DateField()
    cantidad_dias = models.IntegerField('Cantidad de Días')
    estado =        models.CharField('Estado', max_length=10)  #procesado
    autor      =    models.ForeignKey(User, default=2)
    created_at =    models.DateTimeField(auto_now_add=True, blank=True)
    updated_at =    models.DateTimeField(auto_now=True, blank=True)

    def __unicode__(self):
        return self.funcionario.nombre + ' ' + str(self.fecha)

    class Meta:
        verbose_name_plural = 'Solicitudes'

    @models.permalink
    def get_absolute_url(self):
        return 'solicitud_detail', [str(self.id)]

    @models.permalink
    def get_success_url(self):
        return reverse('solicitud_list')


    def get_fechas(self):

        return 'Hola mundo'



class DetalleSolicitud(models.Model):
    solicitud = models.ForeignKey(Solicitud)
    periodo = models.ForeignKey(Periodo)
    fecha = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)


    def __str__(self):
        return str(self.fecha)


    @staticmethod
    def get_fecha_str(index, detalles):
        inicio = index[0]
        fin    = index[1]

        aux = ""

        fecha_inicio_f = detalles[inicio].fecha.strftime('%d/%m/%Y')
        fecha_fin_f    = detalles[fin].fecha.strftime('%d/%m/%Y')

        if inicio == fin:
            aux = fecha_inicio_f
        else: 
            aux = str(fecha_inicio_f) + " al " + str(fecha_fin_f)
        
        return aux


    @staticmethod
    def get_fechas(solicitud_id):
        fechas_str = ""
        lista = []
        detalles = DetalleSolicitud.objects.filter(solicitud=solicitud_id)
        
        inic = 0
        fin = 0
        for fin in range( 1, len(detalles) ):
            delta = detalles[fin].fecha - detalles[fin - 1].fecha
            if delta.days != 1 :
                lista.append( (inic, fin - 1) )
                inic = fin 


        lista.append( (inic, fin) )
        
        if not lista: return ""
        index       = lista.pop(0)
        aux         = DetalleSolicitud.get_fecha_str(index, detalles)
        pre_text = ""
        if fin != 0: pre_text = "Del "

        fechas_str  = pre_text + aux

        for index in lista:
            aux = DetalleSolicitud.get_fecha_str(index, detalles)
            fechas_str +=  ", " + aux

        return fechas_str.encode("utf-8")



