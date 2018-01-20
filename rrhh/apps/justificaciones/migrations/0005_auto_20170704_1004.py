# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('justificaciones', '0004_auto_20170629_0831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='justificacion',
            name='motivo_justificacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='justificaciones.MotivoJustificacion', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='justificacion',
            name='tipo_justificacion',
            field=models.CharField(max_length=3, verbose_name=b'Tipo Justificacion', choices=[(b'fdh', b'Marcaci\xc3\xb3n fuera del horario'), (b'om', b'Omisi\xc3\xb3n de Marcaci\xc3\xb3n')]),
            preserve_default=True,
        ),
    ]
