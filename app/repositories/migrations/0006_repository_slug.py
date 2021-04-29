# Generated by Django 3.0.5 on 2021-04-29 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repositories', '0005_auto_20210403_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='repository',
            name='slug',
            field=models.SlugField(default='default_slug', max_length=200, unique=True),
            preserve_default=False,
        ),
    ]