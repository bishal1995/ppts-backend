# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-29 07:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminofficertoken',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='adminofficertoken',
            name='login_timestamp',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='adminofficertoken',
            name='logout_timestamp',
            field=models.DateTimeField(null=True),
        ),
    ]
