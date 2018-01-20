# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('licencias', '0011_auto_20160930_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='licencia',
            name='autor',
            field=models.ForeignKey(default=2, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
