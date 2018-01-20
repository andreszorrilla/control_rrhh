# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuraciones', '0012_auto_20161117_1238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionario',
            name='estado',
            field=models.CharField(default=b'activo', max_length=9, verbose_name=b'Estado', choices=[(b'activo', b'Activo'), (b'inactivo', b'Inactivo'), (b'pendiente', b'Pendiente')]),
            preserve_default=True,
        ),
    ]
