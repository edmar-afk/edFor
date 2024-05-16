# Generated by Django 5.0.4 on 2024-05-15 10:16

import datetime
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_activity_posted'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='classroom',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.classroom'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lesson',
            name='date_posted',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 15, 10, 16, 27, 694117, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AddField(
            model_name='lesson',
            name='lesson_file',
            field=models.FileField(default=1, upload_to='media/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg', 'docx', 'ppt', 'xls'])]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lesson',
            name='teacher',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='activity',
            name='posted',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 15, 10, 16, 27, 694117, tzinfo=datetime.timezone.utc)),
        ),
    ]
