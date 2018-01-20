# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('justificaciones', '0002_auto_20170614_1446'),
    ]

    operations = [
        migrations.RenameField(
            model_name='justificacion',
            old_name='motivo_marcacion',
            new_name='motivo_justificacion',
        ),
        migrations.AlterField(
            model_name='motivojustificacion',
            name='descripcion',
            field=models.CharField(unique=True, max_length=30),
            preserve_default=True,
        ),
    ]
