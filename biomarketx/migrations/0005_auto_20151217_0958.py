# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-17 09:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biomarketxapp', '0004_users_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='phone',
            field=models.CharField(max_length=15),
        ),
    ]
