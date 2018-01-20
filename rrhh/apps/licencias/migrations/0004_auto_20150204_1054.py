# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('licencias', '0003_auto_20150119_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='licencia',
            name='cantidad_dias',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='licencia',
            name='tipo_documento',
            field=models.CharField(default=b'permiso', max_length=10, verbose_name=b'Tipo dias', choices=[(b'permiso', b'Permiso'), (b'licencia', b'Licencia')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='motivo',
            name='imputable',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
