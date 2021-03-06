# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-04 14:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('malha', '0004_veiculo'),
    ]

    operations = [
        migrations.AddField(
            model_name='veiculo',
            name='lotacao',
            field=models.PositiveIntegerField(default=0, verbose_name='Lota\xe7\xe3o'),
        ),
        migrations.AddField(
            model_name='veiculo',
            name='secret_key',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='Secret Key'),
        ),
        migrations.AlterField(
            model_name='veiculo',
            name='linha',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='veiculos', to='malha.Linha'),
        ),
    ]
