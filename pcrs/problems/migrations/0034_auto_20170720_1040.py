# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-20 14:40
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0033_auto_20170719_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileupload',
            name='lifespan',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 21, 14, 40, 38, 859034, tzinfo=utc), null=True),
        ),
    ]
