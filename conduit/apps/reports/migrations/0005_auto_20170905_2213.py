# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-09-05 22:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0004_auto_20170819_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='mediaTypeCamera1',
            field=models.SmallIntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='report',
            name='mediaTypeCamera2',
            field=models.SmallIntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='report',
            name='mediaTypeCamera3',
            field=models.SmallIntegerField(default=-1),
        ),
    ]
