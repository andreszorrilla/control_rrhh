# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Antiguedad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('anhos_antiguedad', models.IntegerField(unique=True, verbose_name=b'A\xc3\xb1os de Antiguedad', error_messages={b'unique': b'Ya existe una Antiguedad coneste A\xc3\xb1o de Antiguedad.'})),
                ('dias_libres', models.IntegerField(verbose_name=b'D\xc3\xadas Libres')),
            ],
            options={
                'verbose_name': 'Antiguedad',
                'verbose_name_plural': 'Antiguedades',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=90)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=45)),
                ('apellido', models.CharField(max_length=45)),
                ('documento', models.CharField(unique=True, max_length=45, db_index=True)),
                ('fecha_ingreso', models.DateField(verbose_name=b'Fecha de Ingreso')),
                ('estado', models.CharField(default=b'activo', max_length=8, verbose_name=b'Estado', choices=[(b'activo', b'Activo'), (b'inactivo', b'Inactivo')])),
                ('cargo', models.ForeignKey(to='configuraciones.Cargo')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Parametro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('institucion', models.CharField(max_length=45)),
                ('anhos_acumulables_vacaciones', models.IntegerField()),
                ('logo', models.ImageField(upload_to=b'archivos/')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Seccion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=90)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='funcionario',
            name='seccion',
            field=models.ForeignKey(to='configuraciones.Seccion'),
            preserve_default=True,
        ),
    ]
