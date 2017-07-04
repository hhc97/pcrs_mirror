# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-17 14:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import problems.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('problems_rdb', '__first__'),
        ('content', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
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
                ('order_matters', models.BooleanField(default=False)),
                ('challenge', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='problems_sql_problem_related', to='content.Challenge')),
                ('schema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='problems_sql_problem_related', to='problems_rdb.Schema')),
                ('tags', models.ManyToManyField(blank=True, null=True, related_name='problems_sql_problem_related', to='content.Tag')),
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
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problems_sql.Problem')),
                ('section', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='problems_sql_submission_related', to='users.Section')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='problems_sql_submission_related', to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
            options={
                'ordering': ['-timestamp'],
                'abstract': False,
            },
            bases=(problems.models.SubmissionPreprocessorMixin, models.Model),
        ),
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_visible', models.BooleanField(default=False, verbose_name='Testcase visible to students')),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='problems_sql_testcase_related', to='problems_rdb.Dataset')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problems_sql.Problem')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TestRun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_passed', models.BooleanField()),
                ('submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problems_sql.Submission')),
                ('testcase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problems_sql.TestCase')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]