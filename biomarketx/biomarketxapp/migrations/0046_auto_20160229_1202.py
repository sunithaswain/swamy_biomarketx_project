# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-29 12:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biomarketxapp', '0045_message_trash_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='sender_deleted_at',
            field=models.IntegerField(blank=True, null=True, verbose_name='Sender deleted at'),
        ),
    ]
