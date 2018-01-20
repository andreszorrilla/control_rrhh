# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuraciones', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cargo',
            name='nombre',
            field=models.CharField(max_length=45),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='seccion',
            name='nombre',
            field=models.CharField(max_length=45),
            preserve_default=True,
        ),
    ]
