# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.utils.datetime_safe
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('configuraciones', '0005_cargo_seccion'),
    ]

    operations = [
        migrations.AddField(
            model_name='funcionario',
            name='created_at',
            field=models.DateTimeField(default=django.utils.datetime_safe.datetime.now, auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='funcionario',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 29, 12, 42, 30, 105405, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
