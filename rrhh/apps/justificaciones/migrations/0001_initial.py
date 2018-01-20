# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('configuraciones', '0013_auto_20170614_1402'),
    ]

    operations = [
        migrations.CreateModel(
            name='Justicicacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_hora', models.DateTimeField()),
                ('tipo_marcacion', models.CharField(default=b'e', max_length=1, verbose_name=b'Tipo Marcacion', choices=[(b'e', b'Entrada'), (b's', b'Salida')])),
                ('tipo_justificacion', models.CharField(default=b'fdh', max_length=3, verbose_name=b'Tipo Justificacion', choices=[(b'fdh', b'Marcacion fuera del horario'), (b'om', b'Omision de Marcacion')])),
                ('observaciones', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('autor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('funcionario', models.ForeignKey(to='configuraciones.Funcionario')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MotivoJustificacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='justicicacion',
            name='motivo_marcacion',
            field=models.ForeignKey(to='justificaciones.MotivoJustificacion'),
            preserve_default=True,
        ),
    ]