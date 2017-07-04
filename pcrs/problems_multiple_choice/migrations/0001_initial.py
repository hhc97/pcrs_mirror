# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-17 14:51
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
            name='Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.TextField()),
                ('is_correct', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='OptionSelection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('was_selected', models.BooleanField()),
                ('is_correct', models.BooleanField()),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problems_multiple_choice.Option')),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visibility', models.CharField(choices=[('closed', 'closed'), ('open', 'open')], default='open', max_length=10)),
                ('max_score', models.SmallIntegerField(blank=True, default=0)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField()),
                ('no_correct_response', models.BooleanField(default=False)),
                ('challenge', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='problems_multiple_choice_problem_related', to='content.Challenge')),
                ('tags', models.ManyToManyField(blank=True, null=True, related_name='problems_multiple_choice_problem_related', to='content.Tag')),
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
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problems_multiple_choice.Problem')),
                ('section', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='problems_multiple_choice_submission_related', to='users.Section')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='problems_multiple_choice_submission_related', to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
            options={
                'ordering': ['-timestamp'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='optionselection',
            name='submission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problems_multiple_choice.Submission'),
        ),
        migrations.AddField(
            model_name='option',
            name='problem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problems_multiple_choice.Problem'),
        ),
    ]