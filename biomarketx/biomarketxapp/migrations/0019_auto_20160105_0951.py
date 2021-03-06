# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-05 09:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biomarketxapp', '0018_auto_20160104_1736'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExampleModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_pic', models.ImageField(default='pic_folder/None/no-img.jpg', upload_to='pic_folder/')),
            ],
        ),
        migrations.CreateModel(
            name='Labphotos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.FileField(upload_to='Lab-photos')),
            ],
        ),
        migrations.RemoveField(
            model_name='lab',
            name='photo',
        ),
        migrations.AddField(
            model_name='lab',
            name='city',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='lab',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='/media'),
        ),
        migrations.AddField(
            model_name='lab',
            name='state',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='labservices',
            name='url',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
