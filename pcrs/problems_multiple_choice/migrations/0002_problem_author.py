# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-26 19:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems_multiple_choice', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='author',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]