# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-08 12:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biomarketxapp', '0022_researcher_more_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lab',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='media'),
        ),
    ]
