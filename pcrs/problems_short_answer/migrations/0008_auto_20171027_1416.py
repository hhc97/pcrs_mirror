# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-27 18:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems_short_answer', '0007_hstore_extension'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='problems_short_answer_problem_related', to='content.Tag'),
        ),
    ]
