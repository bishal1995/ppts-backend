# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-27 20:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='locationdetails',
            name='timestamp',
            field=models.DateTimeField(null=True),
        ),
    ]