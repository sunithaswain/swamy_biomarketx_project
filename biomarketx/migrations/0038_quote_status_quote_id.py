# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-11 04:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biomarketxapp', '0037_order_status_quote_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote_status',
            name='quote_id',
            field=models.IntegerField(null=True),
        ),
    ]