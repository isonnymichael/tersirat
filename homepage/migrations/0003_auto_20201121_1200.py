# Generated by Django 3.0.5 on 2020-11-21 05:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0002_auto_20201121_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counter',
            name='creation_time',
            field=models.DateField(blank=True, default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='counter',
            name='update_time',
            field=models.DateField(blank=True, default=datetime.date.today),
        ),
    ]
