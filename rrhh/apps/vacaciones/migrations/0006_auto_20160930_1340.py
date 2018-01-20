# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('vacaciones', '0005_solicitud_autor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitud',
            name='autor',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
