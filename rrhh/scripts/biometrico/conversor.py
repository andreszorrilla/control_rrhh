import csv
import sys

from datetime import datetime, date, timedelta
from apps.configuraciones.models import Funcionario, Parametro, Antiguedad, Seccion, Cargo
from apps.vacaciones.models import Periodo
#from dateutil.relativedelta import relativedelta
from datetime import datetime, date
from django.utils import timezone

from apps.biometrico.models import Marcacion, Transaccion

def is_int(value):
	try:
		int(value)
		return True
	except:
		return False

def to_datetime(fecha_hora):
	fecha_hora = fecha_hora.replace(".", "")
	return datetime.strptime(fecha_hora, "%d/%m/%Y %I:%M %p").replace(tzinfo=timezone.utc)

def convertir(dir_archivo):
	hoy	 = datetime.now()
	transaccion = Transaccion(mes=hoy.month, anho=hoy.year)
	transaccion.save()
	with open(dir_archivo, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=';')
		funcionarios_set = set()
		for row in reader:
			if len(row) == 0 or len(row) != 7:
				continue
			elif not is_int(row[0]):
				continue
			else:
				cedula 	= row[0]
				fecha 	= row[2]
				#estado	= row[3]
				fecha_hora = to_datetime(fecha)
				funcionario = Funcionario.objects.filter(estado='activo', documento=cedula).first()
				if funcionario:
					repetido = Marcacion.objects.filter(transaccion=transaccion, funcionario=funcionario, fecha_hora=fecha_hora).count() > 0
					if not repetido:
						marcacion = Marcacion(transaccion=transaccion, funcionario=funcionario, fecha_hora=fecha_hora)
						marcacion.save()
				else:
					if not cedula in funcionarios_set and not Funcionario.objects.filter(estado="pendiente", documento=cedula):
						seccion = Seccion.objects.get_or_create(nombre="--- Seccion No Especificada ---")[0]
						cargo 	= Cargo.objects.get_or_create(nombre="--- Cargo No Especificado ---", seccion_id=seccion.id)[0]
						funcionario = Funcionario( nombre='', apellido='', documento=cedula, estado='pendiente', seccion_id=seccion.id, cargo_id=cargo.id, fecha_ingreso=date.today() )
						funcionario.save()
						funcionarios_set.add(cedula)
	return


convertir("/root/biometrico/2017/junio.csv")