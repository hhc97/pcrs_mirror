# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-27 18:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0006_auto_20171027_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='content_video_related', to='content.Tag'),
        ),
    ]
