# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-12 18:49
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0016_auto_20170612_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileupload',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='fileupload',
            name='lifespan',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 13, 18, 49, 57, 770875, tzinfo=utc), null=True),
        ),
    ]
