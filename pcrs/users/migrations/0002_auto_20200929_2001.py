# Generated by Django 3.1.1 on 2020-09-30 00:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pcrsuser',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.section'),
        ),
    ]
