# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-29 06:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biomarketxapp', '0044_auto_20160229_0641'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='trash_status',
            field=models.IntegerField(null=True, verbose_name='trash_status'),
        ),
    ]
