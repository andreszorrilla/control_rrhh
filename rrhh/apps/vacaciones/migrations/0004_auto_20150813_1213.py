# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('vacaciones', '0003_auto_20150529_1359'),
    ]

    operations = [
        migrations.AddField(
            model_name='detallesolicitud',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 13, 12, 13, 13, 600367, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='detallesolicitud',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 13, 12, 13, 30, 290440, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='estado',
            field=models.CharField(max_length=10, verbose_name=b'Estado'),
            preserve_default=True,
        ),
    ]
