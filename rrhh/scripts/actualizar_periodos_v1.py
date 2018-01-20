from datetime import datetime, date, timedelta
from apps.configuraciones.models import Funcionario, Parametro, Antiguedad
from apps.vacaciones.models import Periodo

def vencer_periodos():
    print "\nControlando Vencimiento de Periodos"
    periodos_activos = Periodo.objects.filter(estado='activo')
    parametro = Parametro.objects.first()
    if not parametro:
        return
    anhos_acumulables = parametro.anhos_acumulables_vacaciones
    for periodo in periodos_activos:
        dia = periodo.funcionario.fecha_ingreso.day
        mes = periodo.funcionario.fecha_ingreso.month
        anho = periodo.anho
        fecha = str(dia) + '/' + str(mes) + '/' + str(anho)
        if cantidad_anhos_desde(fecha) > anhos_acumulables:
            print "Periodo vencido de: " + periodo.funcionario.nombre + " del anho " + str(anho)
            periodo.estado = 'vencido'
            periodo.save()

def crear_periodos():
    print "\n\nCargando Vacaciones..."
    funcionarios = Funcionario.objects.filter(estado='activo')
    hoy = datetime.now()
    print hoy
    for funcionario in funcionarios:
        fecha_de_actualizacion = datetime(hoy.year, funcionario.fecha_ingreso.month, funcionario.fecha_ingreso.day)
        print '\n{0}: fecha actualizacion {1}'.format(funcionario, fecha_de_actualizacion.date())
        if hoy.date() >= fecha_de_actualizacion.date():
            print 'Actualizar: Si'
            anhos_antiguedad = cantidad_anhos_desde(
                str(funcionario.fecha_ingreso.day) + '/' + str(funcionario.fecha_ingreso.month) + '/' + str(funcionario.fecha_ingreso.year))
            print 'Anhos de Antiguedad: ', anhos_antiguedad
            antiguedad = None
            try:
                antiguedad = Antiguedad.objects.filter(anhos_antiguedad__lte=anhos_antiguedad).order_by('-anhos_antiguedad')[:1].get()
                if not antiguedad:
                    print "No se puede tener vacaciones con " + str(anhos_antiguedad) + " anhos"
                    continue
            except Exception, e:
                print "No se puede tener vacaciones con " + str(anhos_antiguedad) + " anhos"
                continue
            print 'Dias Libres: ', antiguedad.dias_libres
            periodo, created = Periodo.objects.get_or_create(anho=(hoy.year - 1), funcionario_id=funcionario.id, defaults={'total': antiguedad.dias_libres, 'usados': 0, 'libres': antiguedad.dias_libres})
            if created:
                print 'Periodo {0} creado'.format(hoy.year)
            else:
                print 'Periodo {0} ya existe'.format(hoy.year)
        else:
            print 'Actualizar: No'

def antiguedad_anhos(fecha_desde):
    before = datetime.strptime(fecha_desde, '%d/%m/%Y')
    now = datetime.now()
    dates = [ now.replace(year = now.year - i - 1) for i in range(2) ] # CANTIDAD ANHOS ACUMULABLES
    return [abs( (date - before).days )  / 365 for date in dates ]  


def antiguedad_anhos_v2(fecha_desde):

    fecha_ingreso = datetime.strptime(fecha_desde, '%d/%m/%Y')
    now = datetime.now()
    fecha_habilitacion_periodo = fecha_ingreso.replace(year = now.year)
    #print "************"
    #print fecha_habilitacion_periodo
    #print "************"
    dates = []
    cantidad_dias = []
    fechas = []
    for i in range(2): # CANTIDAD ANHOS ACUMULABLES
        fecha_periodo = fecha_ingreso.replace(year = now.year - i - 1)
        if fecha_periodo < fecha_ingreso: break
        fechas.append( fecha_periodo )
        if True :
            if fecha_ingreso < fecha_periodo:
                cantidad_dias.append( (fecha_periodo  - fecha_ingreso).days / 365 )
            else:
                cantidad_dias.append( (now  - fecha_periodo).days / 365 )
    return cantidad_dias


def crear_periodos_v2():
    print "\n\nCargando Vacaciones..."
    funcionarios = Funcionario.objects.all()
    hoy = datetime.now()
    for funcionario in funcionarios:
        fecha_de_actualizacion = datetime(hoy.year, funcionario.fecha_ingreso.month, funcionario.fecha_ingreso.day)
        print '\n{0}: fecha actualizacion {1}'.format(funcionario, fecha_de_actualizacion.date())
        if True:
            print 'Actualizar: Si'
            anhos_antiguedad = antiguedad_anhos_v2(str(funcionario.fecha_ingreso.day) + '/' + str(funcionario.fecha_ingreso.month) + '/' + str(funcionario.fecha_ingreso.year))
            
            for i, cantidad_anho in enumerate(anhos_antiguedad):
                antiguedad = None
                try:
                    antiguedad = Antiguedad.objects.filter(anhos_antiguedad__lte=cantidad_anho).order_by('-anhos_antiguedad')[:1].get()
                    if not antiguedad:
                        print "No se puede tener vacaciones con " + str(cantidad_anho) + " anhos"
                        continue
                except Exception, e:
                    print "No se puede tener vacaciones con " + str(cantidad_anho) + " anhos"
                    continue
                print 'Dias Libres: ', antiguedad.dias_libres
                periodo, created = Periodo.objects.get_or_create(anho=(hoy.year - i - 1), funcionario_id=funcionario.id, defaults={'total': antiguedad.dias_libres, 'usados': 0, 'libres': antiguedad.dias_libres})
                if created:
                    print 'Periodo {0} creado'.format(hoy.year)
                else:
                    print 'Periodo {0} ya existe'.format(hoy.year)
        else:
            print 'Actualizar: No'

def cantidad_anhos_desde(fecha_desde):
    before = datetime.strptime(fecha_desde, '%d/%m/%Y')
    now = datetime.now()
    type(now - before)
    return (now - before).days / 365



#Periodo.objects.all().delete()
crear_periodos_v2()
vencer_periodos()