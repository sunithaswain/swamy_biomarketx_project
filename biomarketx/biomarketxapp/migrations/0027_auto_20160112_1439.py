# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-12 14:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biomarketxapp', '0026_auto_20160111_0014'),
    ]

    operations = [
        migrations.CreateModel(
            name='LabProfilepic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_pic', models.ImageField(blank=True, null=True, upload_to='images')),
            ],
        ),
        migrations.DeleteModel(
            name='Profilepic',
        ),
        migrations.AlterModelOptions(
            name='users',
            options={'get_latest_by': 'created_at'},
        ),
    ]