# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-21 09:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biomarketxapp', '0014_auto_20151221_0903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labendorse',
            name='lab_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='labreviews',
            name='lab_id',
            field=models.IntegerField(),
        ),
    ]