# Generated by Django 3.0.5 on 2021-03-28 20:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0007_testissue_repository'),
    ]

    operations = [
        migrations.AddField(
            model_name='testissue',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]