# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-18 11:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biomarketxapp', '0005_auto_20151217_0958'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='how_bio',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]