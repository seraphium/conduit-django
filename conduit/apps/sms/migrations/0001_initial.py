# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-07-31 07:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('units', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('time', models.DateTimeField()),
                ('content', models.CharField(max_length=255)),
                ('direction', models.SmallIntegerField(choices=[(0, 'send'), (1, 'receive')])),
                ('sender', models.CharField(max_length=32)),
                ('receiver', models.CharField(max_length=32)),
                ('state', models.SmallIntegerField()),
                ('checksumcorrect', models.BooleanField()),
                ('iotid', models.CharField(blank=True, max_length=255)),
                ('device', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sms', to='units.Unit')),
            ],
            options={
                'ordering': ['-created_at', '-updated_at'],
                'abstract': False,
            },
        ),
    ]
