# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-09 05:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biomarketxapp', '0023_auto_20160108_1241'),
    ]

    operations = [
        migrations.CreateModel(
            name='image_details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='pic_folder/None/no-img.jpg', upload_to='media/')),
            ],
        ),
    ]
