# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-17 14:34
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SectionQuestPosition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.IntegerField()),
                ('y', models.IntegerField()),
                ('content_sectionquest', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='content.SectionQuest')),
            ],
            options={
                'db_table': 'content_sectionquest_positions',
            },
        ),
    ]
