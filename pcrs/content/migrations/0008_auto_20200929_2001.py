# Generated by Django 3.1.1 on 2020-09-30 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0007_auto_20171027_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='enforce_prerequisites',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='is_graded',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
