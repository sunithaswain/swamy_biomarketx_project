# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-04 08:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('biomarketxapp', '0054_workroom_files'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workroom_files',
            old_name='order_id',
            new_name='workroom_id',
        ),
    ]
