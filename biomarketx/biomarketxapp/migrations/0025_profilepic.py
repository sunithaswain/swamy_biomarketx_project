# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-09 07:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biomarketxapp', '0024_image_details'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profilepic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_pic', models.ImageField(blank=True, null=True, upload_to='satya')),
            ],
        ),
    ]
