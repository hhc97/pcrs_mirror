# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-09 12:32
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0010_auto_20170608_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileupload',
            name='lifespan',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 10, 12, 32, 12, 641854, tzinfo=utc), null=True),
        ),
    ]
