# Generated by Django 3.0.5 on 2021-04-10 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0016_auto_20210409_0849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='body',
            field=models.TextField(blank=True, null=True),
        ),
    ]
