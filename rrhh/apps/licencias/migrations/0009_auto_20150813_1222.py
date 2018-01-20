# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('licencias', '0008_auto_20150813_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='motivo',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
            preserve_default=True,
        ),
    ]
