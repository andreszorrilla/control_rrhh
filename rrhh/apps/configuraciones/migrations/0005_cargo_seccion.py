# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuraciones', '0004_auto_20150113_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='cargo',
            name='seccion',
            field=models.ForeignKey(default=1, to='configuraciones.Seccion'),
            preserve_default=False,
        ),
    ]
