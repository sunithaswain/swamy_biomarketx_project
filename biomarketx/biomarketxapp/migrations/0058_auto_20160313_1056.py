# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-13 10:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biomarketxapp', '0057_edit_about'),
    ]

    operations = [
        migrations.AddField(
            model_name='labservices',
            name='service_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='services',
            name='admin_status',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='researcher_more_info',
            name='model_pic',
            field=models.ImageField(blank=True, null=True, upload_to='pic_folder'),
        ),
    ]
