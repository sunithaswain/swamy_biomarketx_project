# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-09 07:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biomarketxapp', '0034_book'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sid', models.IntegerField()),
                ('researcher_id', models.IntegerField()),
                ('lab_id', models.IntegerField()),
                ('desc', models.TextField()),
                ('notes', models.TextField()),
                ('price', models.FloatField()),
                ('duration', models.CharField(max_length=250)),
                ('memo', models.CharField(max_length=250)),
                ('status_id', models.IntegerField()),
                ('service_id', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Quote_files',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quote_id', models.IntegerField()),
                ('filename', models.FileField(upload_to='quotes')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Quote_payments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quote_id', models.IntegerField()),
                ('amount', models.FloatField()),
                ('status', models.CharField(max_length=250)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Quotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sid', models.CharField(blank=True, max_length=250)),
                ('researcher_id', models.IntegerField()),
                ('researcher_name', models.CharField(blank=True, max_length=250)),
                ('lab_id', models.IntegerField()),
                ('service_id', models.IntegerField(null=True)),
                ('service_name', models.CharField(blank=True, max_length=250)),
                ('desc', models.TextField()),
                ('notes', models.TextField()),
                ('price', models.FloatField(null=True)),
                ('duration', models.CharField(blank=True, max_length=250)),
                ('memo', models.CharField(blank=True, max_length=250)),
                ('status_id', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Quotes_msgs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quote_id', models.IntegerField()),
                ('body', models.TextField()),
                ('msg_status', models.CharField(max_length=250)),
                ('sender_id', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.IntegerField()),
                ('name', models.CharField(max_length=300)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField()),
            ],
        ),
        migrations.RemoveField(
            model_name='active_jobs',
            name='job_id',
        ),
        migrations.RemoveField(
            model_name='files',
            name='job_id',
        ),
        migrations.RemoveField(
            model_name='lab_quote',
            name='lab_id',
        ),
        migrations.RemoveField(
            model_name='messages',
            name='job_id',
        ),
        migrations.DeleteModel(
            name='ParentServices',
        ),
        migrations.RemoveField(
            model_name='quote_order',
            name='user_id',
        ),
        migrations.DeleteModel(
            name='Quote_status',
        ),
        migrations.RemoveField(
            model_name='researcher_quote',
            name='user_id',
        ),
        migrations.DeleteModel(
            name='Service',
        ),
        migrations.RenameField(
            model_name='labmembers',
            old_name='lab_id',
            new_name='lab',
        ),
        migrations.AddField(
            model_name='lab',
            name='service_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Active_jobs',
        ),
        migrations.DeleteModel(
            name='Files',
        ),
        migrations.DeleteModel(
            name='Job',
        ),
        migrations.DeleteModel(
            name='Lab_quote',
        ),
        migrations.DeleteModel(
            name='Messages',
        ),
        migrations.DeleteModel(
            name='Quote_order',
        ),
        migrations.DeleteModel(
            name='Researcher_quote',
        ),
    ]
