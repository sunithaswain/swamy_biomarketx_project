# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-01 10:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biomarketxapp', '0047_remove_message_trash_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='researcher_name',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='orders',
            name='sent_by',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='orders',
            name='service_name',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='orders',
            name='duration',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='orders',
            name='memo',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='orders',
            name='price',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='service_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='sid',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
