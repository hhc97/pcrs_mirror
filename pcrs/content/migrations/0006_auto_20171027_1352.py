# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-27 17:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0005_description_optional'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='prerequisites',
            field=models.ManyToManyField(blank=True, to='content.Challenge'),
        ),
    ]
