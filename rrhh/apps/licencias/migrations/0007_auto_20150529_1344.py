# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('licencias', '0006_auto_20150226_1243'),
    ]

    operations = [
        migrations.AddField(
            model_name='feriados',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 29, 13, 44, 25, 313283, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='feriados',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 29, 13, 44, 29, 367424, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='licencia',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 29, 13, 44, 33, 118817, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='licencia',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 29, 13, 44, 37, 960938, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='motivo',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 29, 13, 44, 40, 846990, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='motivo',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 29, 13, 44, 43, 996569, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
