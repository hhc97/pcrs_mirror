# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-19 14:51
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0025_auto_20170719_1036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileupload',
            name='lifespan',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 20, 14, 51, 5, 164929, tzinfo=utc), null=True),
        ),
    ]
