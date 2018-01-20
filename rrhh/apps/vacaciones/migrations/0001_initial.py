# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuraciones', '0003_auto_20150108_1415'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetalleSolicitud',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Periodo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('anho', models.IntegerField(max_length=4, verbose_name=b'A\xc3\xb1o')),
                ('total', models.IntegerField()),
                ('usados', models.IntegerField()),
                ('libres', models.IntegerField()),
                ('estado', models.CharField(default=b'activo', max_length=8, verbose_name=b'Estado', choices=[(b'activo', b'Activo'), (b'vencido', b'Vencido')])),
                ('funcionario', models.ForeignKey(to='configuraciones.Funcionario')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.IntegerField()),
                ('fecha_emision', models.DateField(auto_now=True)),
                ('fecha', models.DateField()),
                ('cantidad_dias', models.IntegerField(verbose_name=b'Cantidad de D\xc3\xadas')),
                ('estado', models.CharField(max_length=8, verbose_name=b'Estado')),
                ('funcionario', models.ForeignKey(to='configuraciones.Funcionario')),
            ],
            options={
                'verbose_name_plural': 'Solicitudes',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='detallesolicitud',
            name='periodo',
            field=models.ForeignKey(to='vacaciones.Periodo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='detallesolicitud',
            name='solicitud',
            field=models.ForeignKey(to='vacaciones.Solicitud'),
            preserve_default=True,
        ),
    ]
