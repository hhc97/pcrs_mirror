# Generated by Django 3.1.7 on 2021-03-10 20:32

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0004_auto_20200929_2001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileupload',
            name='lifespan',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 11, 20, 32, 54, 247945, tzinfo=utc), null=True),
        ),
    ]