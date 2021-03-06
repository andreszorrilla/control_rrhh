# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('licencias', '0009_auto_20150813_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='licencia',
            name='autor',
            field=models.ForeignKey(default=2, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
