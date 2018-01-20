# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vacaciones', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitud',
            name='numero',
            field=models.IntegerField(null=True, verbose_name=b'Numero de solicitud'),
            preserve_default=True,
        ),
    ]
