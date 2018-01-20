# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('configuraciones', '0010_auto_20160930_1224'),
    ]

    operations = [
        migrations.AddField(
            model_name='seccion',
            name='group',
            field=models.ForeignKey(default=1, to='auth.Group'),
            preserve_default=True,
        ),
    ]
