# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-08-19 09:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0003_auto_20170807_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='ackDetail',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='mediaGuid',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]