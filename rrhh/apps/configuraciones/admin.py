from django.contrib import admin

from .models import Antiguedad, Funcionario, Parametro


admin.site.register(Antiguedad)
admin.site.register(Funcionario)
admin.site.register(Parametro)