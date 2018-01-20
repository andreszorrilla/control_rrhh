# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('licencias', '0005_auto_20150209_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='motivo',
            name='tipo_motivo',
            field=models.CharField(default=b'habiles', max_length=10, verbose_name=b'Tipo dias', choices=[(b'habiles', b'Dias habiles'), (b'corridos', b'Dias corridos'), (b'permiso', b'Permiso')]),
            preserve_default=True,
        ),
    ]
