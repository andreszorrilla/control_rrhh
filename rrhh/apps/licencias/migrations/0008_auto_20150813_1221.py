# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('licencias', '0007_auto_20150529_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feriados',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
            preserve_default=True,
        ),
    ]
