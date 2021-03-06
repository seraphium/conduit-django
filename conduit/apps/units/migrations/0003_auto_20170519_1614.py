# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-05-19 08:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('units', '0002_auto_20170519_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='backupcarrier',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='unit',
            name='carrier',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='unit',
            name='gprsstatus',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='unit',
            name='hardwareversion',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='unit',
            name='idintower',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='unit',
            name='lat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='unit',
            name='lng',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='unit',
            name='operators',
            field=models.ManyToManyField(blank=True, related_name='units', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='unit',
            name='powerstatus',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='unit',
            name='protocolversion',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='unit',
            name='status',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='unit',
            name='temperature',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='unit',
            name='towerfrom',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='unit',
            name='towerto',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='unit',
            name='vendor',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
    ]
