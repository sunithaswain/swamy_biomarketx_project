# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-21 06:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('biomarketxapp', '0011_labservices_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lab',
            name='labendorse_id',
        ),
        migrations.RemoveField(
            model_name='lab',
            name='labreviews_id',
        ),
        migrations.RemoveField(
            model_name='lab',
            name='labservices_id',
        ),
    ]
