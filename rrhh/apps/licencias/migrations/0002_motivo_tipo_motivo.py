# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('licencias', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='motivo',
            name='tipo_motivo',
            field=models.CharField(default=b'habiles', max_length=10, verbose_name=b'Tipo motivo', choices=[(b'habiles', b'Dias habiles'), (b'corridos', b'Dias corridos')]),
            preserve_default=True,
        ),
    ]
