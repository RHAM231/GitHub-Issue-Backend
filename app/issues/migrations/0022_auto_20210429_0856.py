# Generated by Django 3.0.5 on 2021-04-29 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0021_auto_20210424_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='slug',
            field=models.SlugField(max_length=200, unique=True),
        ),
    ]