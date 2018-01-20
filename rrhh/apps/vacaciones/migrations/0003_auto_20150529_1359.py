# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('vacaciones', '0002_auto_20150108_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='periodo',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 29, 13, 59, 7, 159344, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='periodo',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 29, 13, 59, 3, 854637, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='solicitud',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 29, 13, 59, 7, 159344, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='solicitud',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 29, 13, 59, 9, 636424, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
