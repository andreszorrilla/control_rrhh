# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuraciones', '0003_auto_20150108_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionario',
            name='cargo',
            field=models.ForeignKey(to='configuraciones.Cargo'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='seccion',
            field=models.ForeignKey(to='configuraciones.Seccion'),
            preserve_default=True,
        ),
    ]
