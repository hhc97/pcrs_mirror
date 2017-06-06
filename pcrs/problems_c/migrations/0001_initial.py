# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-17 14:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('content', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='JobScheduler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('protocol', models.CharField(blank=True, max_length=16)),
                ('ip', models.CharField(blank=True, max_length=16)),
                ('dns', models.CharField(blank=True, max_length=200)),
                ('port', models.CharField(blank=True, max_length=10)),
                ('api_url', models.CharField(blank=True, max_length=100)),
                ('user', models.CharField(blank=True, max_length=100)),
                ('password', models.CharField(blank=True, max_length=100)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('visibility', models.CharField(choices=[('closed', 'closed'), ('open', 'open')], default='open', max_length=10)),
                ('max_score', models.SmallIntegerField(blank=True, default=0)),
                ('starter_code', models.TextField(blank=True)),
                ('solution', models.TextField(blank=True)),
                ('language', models.CharField(choices=[('c', 'C')], default='c', max_length=50)),
                ('challenge', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='problems_c_problem_related', to='content.Challenge')),
                ('tags', models.ManyToManyField(blank=True, null=True, related_name='problems_c_problem_related', to='content.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('submission', models.TextField(blank=True, null=True)),
                ('score', models.SmallIntegerField(default=0)),
                ('has_best_score', models.BooleanField(default=False)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problems_c.Problem')),
                ('section', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='problems_c_submission_related', to='users.Section')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='problems_c_submission_related', to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
            options={
                'ordering': ['-timestamp'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_visible', models.BooleanField(default=False, verbose_name='Testcase visible to students')),
                ('description', models.TextField(blank=True)),
                ('test_input', models.TextField()),
                ('expected_output', models.TextField()),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problems_c.Problem')),
            ],
            options={
                'ordering': ['pk'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TestRun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_passed', models.BooleanField()),
                ('submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problems_c.Submission')),
                ('testcase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problems_c.TestCase')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
