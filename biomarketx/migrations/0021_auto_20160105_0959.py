# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-05 09:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biomarketxapp', '0020_auto_20160105_0957'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='users',
            name='username',
            field=models.CharField(default=0, max_length=250),
            preserve_default=False,
        ),
    ]
