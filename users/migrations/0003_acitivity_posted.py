# Generated by Django 5.0.4 on 2024-05-13 01:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_passactivity_activity_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='acitivity',
            name='posted',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 13, 1, 14, 53, 772419, tzinfo=datetime.timezone.utc)),
        ),
    ]
