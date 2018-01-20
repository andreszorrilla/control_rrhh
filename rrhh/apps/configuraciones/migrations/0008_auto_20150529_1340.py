# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('configuraciones', '0007_auto_20150529_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='antiguedad',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 29, 13, 38, 55, 449284, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='antiguedad',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 29, 13, 39, 6, 40699, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cargo',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 29, 13, 39, 16, 271354, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cargo',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 29, 13, 39, 25, 821910, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parametro',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 29, 13, 39, 36, 181211, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parametro',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 29, 13, 39, 59, 475346, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='seccion',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 29, 13, 40, 3, 699720, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='seccion',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 29, 13, 40, 6, 757395, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
