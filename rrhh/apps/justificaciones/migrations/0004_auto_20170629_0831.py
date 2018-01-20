# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('justificaciones', '0003_auto_20170628_1359'),
    ]

    operations = [
        migrations.AddField(
            model_name='justificacion',
            name='estado',
            field=models.CharField(default=b'activo', max_length=9, verbose_name=b'Estado', choices=[(b'activo', b'Activo'), (b'inactivo', b'Inactivo')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='justificacion',
            name='motivo_justificacion',
            field=models.ForeignKey(to='justificaciones.MotivoJustificacion', on_delete=django.db.models.deletion.PROTECT),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='justificacion',
            name='tipo_justificacion',
            field=models.CharField(max_length=3, verbose_name=b'Tipo Justificacion', choices=[(b'fdh', b'Marcacion fuera del horario'), (b'om', b'Omision de Marcacion')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='justificacion',
            name='tipo_marcacion',
            field=models.CharField(max_length=1, verbose_name=b'Tipo Marcacion', choices=[(b'e', b'Entrada'), (b's', b'Salida')]),
            preserve_default=True,
        ),
    ]
