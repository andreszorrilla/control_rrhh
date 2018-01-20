# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('licencias', '0002_motivo_tipo_motivo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feriados',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField(verbose_name=b'fecha')),
                ('motivo', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='motivo',
            name='tipo_motivo',
            field=models.CharField(default=b'habiles', max_length=10, verbose_name=b'Tipo dias', choices=[(b'habiles', b'Dias habiles'), (b'corridos', b'Dias corridos')]),
            preserve_default=True,
        ),
    ]
