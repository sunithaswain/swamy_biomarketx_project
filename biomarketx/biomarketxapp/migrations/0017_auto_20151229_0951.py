# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-29 09:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biomarketxapp', '0016_auto_20151221_0927'),
    ]

    operations = [
        migrations.AddField(
            model_name='lab',
            name='core_facility',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='lab',
            name='orgname',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='lab',
            name='typeorg',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
