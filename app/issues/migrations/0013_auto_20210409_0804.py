# Generated by Django 3.0.5 on 2021-04-09 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0012_auto_20210409_0751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='closed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
