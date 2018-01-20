# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuraciones', '0009_funcionario_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionario',
            name='group',
            field=models.ForeignKey(default=1, to='auth.Group'),
            preserve_default=True,
        ),
    ]
