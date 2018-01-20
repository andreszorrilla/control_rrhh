# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuraciones', '0012_auto_20161117_1238'),
    ]

    operations = [
        migrations.CreateModel(
            name='Marcacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_hora', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('estado', models.CharField(default=b'activo', max_length=9, verbose_name=b'Estado', choices=[(b'activo', b'Aactivo'), (b'inactivo', b'Inactivo')])),
                ('funcionario', models.ForeignKey(to='configuraciones.Funcionario')),
            ],
            options={
                'verbose_name_plural': 'Marcaciones',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transaccion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mes', models.IntegerField()),
                ('anho', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='marcacion',
            name='transaccion',
            field=models.ForeignKey(to='biometrico.Transaccion'),
            preserve_default=True,
        ),
    ]
