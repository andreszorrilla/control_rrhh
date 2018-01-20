# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuraciones', '0004_auto_20150113_1136'),
    ]

    operations = [
        migrations.CreateModel(
            name='Licencia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_solicitud', models.DateField(verbose_name=b'Fecha solicitud')),
                ('fecha_inicio', models.DateField(verbose_name=b'Inicio')),
                ('fecha_fin', models.DateField(verbose_name=b'Fin')),
                ('estado', models.CharField(default=b'activo', max_length=8, verbose_name=b'Estado', choices=[(b'activo', b'Activo'), (b'inactivo', b'Inactivo')])),
                ('funcionario', models.ForeignKey(to='configuraciones.Funcionario')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Motivo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=50)),
                ('duracion', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='licencia',
            name='motivo',
            field=models.ForeignKey(to='licencias.Motivo'),
            preserve_default=True,
        ),
    ]
