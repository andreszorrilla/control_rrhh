# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuraciones', '0011_seccion_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='funcionario',
            name='email',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='funcionario',
            name='fecha_nacimiento',
            field=models.DateField(null=True, verbose_name=b'Fecha de Nacimiento', blank=True),
            preserve_default=True,
        ),
    ]
