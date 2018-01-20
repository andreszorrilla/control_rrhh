from datetime import datetime, date, timedelta
from apps.configuraciones.models import Funcionario, Parametro, Antiguedad
from apps.vacaciones.models import Periodo
from dateutil.relativedelta import relativedelta

def vencer_periodos():
		print "\nControlando Vencimiento de Periodos"
		periodos_activos = Periodo.objects.filter(estado='activo')
		parametro 		 = Parametro.objects.first()
		hoy				 = date.today()
		if not parametro:
				return
		anhos_acumulables = parametro.anhos_acumulables_vacaciones
		for periodo in periodos_activos:
				funcionario = periodo.funcionario
				fecha_periodo = date(periodo.anho, funcionario.fecha_ingreso.month, funcionario.fecha_ingreso.day)
				anhos_antiguedad_periodo = relativedelta(hoy, fecha_periodo).years
				if anhos_antiguedad_periodo > anhos_acumulables:
					print "Periodo vencido de: " + periodo.funcionario.nombre.encode('utf-8') + " del anho " + str(periodo.anho)
					periodo.estado = "vencido"
					periodo.save()

def get_antiguedad( cantidad_anho ):
	antiguedad = None
	try:
		antiguedad = Antiguedad.objects.filter(anhos_antiguedad__lte=cantidad_anho).order_by('-anhos_antiguedad')[:1].get()
		if not antiguedad:
			return None
	except Exception, e:
		return None
	return antiguedad

def crear_periodos():
	funcionarios	= Funcionario.objects.filter(estado='activo')
	hoy				= datetime.now()
	for funcionario in funcionarios:
		fecha_ingreso	= datetime.combine(funcionario.fecha_ingreso, datetime.min.time())
		for i in range(2):
			fecha_actualizacion = datetime(hoy.year - i, funcionario.fecha_ingreso.month, funcionario.fecha_ingreso.day)
			if hoy >= fecha_actualizacion:
				print '{0}: fecha actualizacion {1}'.format(funcionario, fecha_actualizacion.date())
				print '{0}: fecha ingreso {1}'.format(funcionario, fecha_ingreso.date())
				dias_restantes = (fecha_actualizacion  - fecha_ingreso ).days + 8
				print "Dias restantes: ", (fecha_actualizacion  - fecha_ingreso ).days, " <---------> ", dias_restantes
				antiguedad = get_antiguedad( dias_restantes / 365.0 )
				if antiguedad != None:
					periodo, created = Periodo.objects.get_or_create(anho=fecha_actualizacion.year - 1, funcionario_id=funcionario.id, defaults={'total': antiguedad.dias_libres, 'usados': 0, 'libres': antiguedad.dias_libres})
		print '\n'

####
### print "Eliminando todos los periodos"
### return
#Periodo.objects.all().delete()
###
###

crear_periodos()
vencer_periodos()