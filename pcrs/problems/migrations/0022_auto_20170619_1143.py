# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-19 15:43
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0021_auto_20170619_1018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileupload',
            name='lifespan',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 20, 15, 43, 25, 416809, tzinfo=utc), null=True),
        ),
    ]
