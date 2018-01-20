# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('licencias', '0004_auto_20150204_1054'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetalleLicencia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField()),
                ('licencia', models.ForeignKey(to='licencias.Licencia')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='motivo',
            name='imputable',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
