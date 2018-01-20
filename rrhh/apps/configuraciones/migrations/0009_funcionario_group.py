# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('configuraciones', '0008_auto_20150529_1340'),
    ]

    operations = [
        migrations.AddField(
            model_name='funcionario',
            name='group',
            field=models.ForeignKey(default=2, to='auth.Group'),
            preserve_default=True,
        ),
    ]
