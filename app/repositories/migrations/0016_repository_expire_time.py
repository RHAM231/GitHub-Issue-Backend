# Generated by Django 3.0.5 on 2021-05-27 22:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('repositories', '0015_auto_20210524_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='repository',
            name='expire_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
