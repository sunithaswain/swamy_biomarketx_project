# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-04 09:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biomarketxapp', '0055_auto_20160304_0843'),
    ]

    operations = [
        migrations.AddField(
            model_name='workroom_files',
            name='order_id',
            field=models.IntegerField(null=True),
        ),
    ]
