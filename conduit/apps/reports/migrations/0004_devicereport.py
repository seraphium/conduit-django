# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-05-19 09:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('units', '0003_auto_20170519_1614'),
        ('reports', '0003_auto_20170519_1625'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('time', models.DateTimeField()),
                ('temperature', models.IntegerField(blank=True, null=True)),
                ('csq', models.IntegerField()),
                ('mode', models.IntegerField()),
                ('resetcount', models.IntegerField()),
                ('networkstatus', models.IntegerField()),
                ('protocolversion', models.IntegerField()),
                ('hardwareversion', models.IntegerField()),
                ('softwareversion', models.IntegerField()),
                ('picresolution', models.CharField(max_length=32)),
                ('picenable', models.BooleanField()),
                ('piclightenhance', models.BooleanField()),
                ('highsensitivity', models.BooleanField()),
                ('beep', models.BooleanField()),
                ('status', models.SmallIntegerField(blank=True, null=True)),
                ('powerstatus', models.SmallIntegerField(blank=True, null=True)),
                ('gprsstatus', models.SmallIntegerField(blank=True, null=True)),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='devicereports', to='units.Unit')),
            ],
            options={
                'abstract': False,
                'ordering': ['-created_at', '-updated_at'],
            },
        ),
    ]
