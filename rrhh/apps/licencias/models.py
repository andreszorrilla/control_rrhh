from django.db import models
from apps.configuraciones.models import Funcionario
from django.contrib.auth.models import User


class Feriados(models.Model):
    fecha = models.DateField('fecha')
    motivo = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)


# Motivos de licencias y duraciones
class Motivo(models.Model):
    descripcion = models.CharField(max_length=50)
    duracion    = models.IntegerField()
    
    OPCIONES_TIPO_MOTIVO = (('habiles', 'Dias habiles'), ('corridos', 'Dias corridos'), ('permiso', 'Permiso'))
    tipo_motivo = models.CharField('Tipo dias', choices=OPCIONES_TIPO_MOTIVO, default='habiles', max_length=10)

    imputable = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return (self.descripcion + " - " + self.tipo_motivo).encode('utf-8')

    def get_duracion_detallada(self):
        return (str(self.duracion) + " dias " + self.tipo_motivo).encode('utf-8')


class Licencia(models.Model):
    fecha_solicitud = models.DateField('Fecha solicitud')
    fecha_inicio    = models.DateField('Inicio')
    fecha_fin       = models.DateField('Fin')
    funcionario     = models.ForeignKey(Funcionario)    
    motivo          = models.ForeignKey(Motivo)
    autor           = models.ForeignKey(User, default=2)

    OPCIONES = (
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    )
    estado = models.CharField('Estado', choices=OPCIONES, default='activo', max_length=8)
    cantidad_dias   = models.IntegerField(default=0)

    OPCIONES_TIPO_DOCUMENTO = (
        ('permiso', 'Permiso'), 
        ('licencia', 'Licencia')
    )
    tipo_documento  = models.CharField('Tipo dias', choices=OPCIONES_TIPO_DOCUMENTO, default='permiso', max_length=10)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)


    """
        Verificamos si existe una licencia con estado activo segun una fecha pasada.
        Si existe retornamos la licencia
        Si no, retornamos None

        argumentos: 
        fecha: tipo Date
        funcionario: de la clase Funcionario
    """
    @staticmethod
    def exist_by_fecha(fecha, funcionario):
        # Si existe 
        licencia = Licencia.objects.filter( fecha_fin__gte=fecha, 
                                            fecha_inicio__lte=fecha,
                                            funcionario=funcionario,
                                            estado="activo",
                                            motivo__tipo_motivo="corridos").first()
        if not licencia is None:
            return licencia
        detalle = DetalleLicencia.objects.filter(   fecha=fecha,
                                                    licencia__funcionario=funcionario,
                                                    licencia__estado="activo").first()
        if not detalle is None:
            return detalle.licencia
        return None

class DetalleLicencia(models.Model):
    licencia = models.ForeignKey(Licencia)
    fecha = models.DateField()

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
    def get_fechas(licencia_id):
        fechas_str = ""
        lista = []

        licencia = Licencia.objects.get(pk=licencia_id)
        tipo_motivo = licencia.motivo.tipo_motivo

        if tipo_motivo == "corridos":
            return ""

        detalles = DetalleLicencia.objects.filter(licencia=licencia_id)
        
        inic = 0
        fin = 0

        for fin in range( 1, len(detalles) ):
            delta = detalles[fin].fecha - detalles[fin - 1].fecha
            if delta.days != 1 :
                lista.append( (inic, fin - 1) )
                inic = fin 
        lista.append( (inic, fin) )
        
        if not lista:
            return ""

        for l in lista:
            print l
            print ""

        index       = lista.pop(0)
        aux         = DetalleLicencia.get_fecha_str(index, detalles)
        
        pre_text = ""
        if fin != 0: pre_text = "Del "

        fechas_str  = pre_text + aux

        for index in lista:
            aux = DetalleLicencia.get_fecha_str(index, detalles)
            fechas_str +=  ", " + aux

        return fechas_str.encode('utf-8')
