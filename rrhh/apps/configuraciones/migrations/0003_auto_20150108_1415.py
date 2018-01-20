# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuraciones', '0002_auto_20150108_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionario',
            name='cargo',
            field=models.ForeignKey(to='configuraciones.Cargo', choices=[(1, 'Tecnico Informatico')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='seccion',
            field=models.ForeignKey(to='configuraciones.Seccion', choices=[(1, 'Departamento de Informatica')]),
            preserve_default=True,
        ),
    ]
