# Generated by Django 3.0.5 on 2021-04-29 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repositories', '0010_repofile_issuetracker_url_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='repofile',
            name='slug',
            field=models.SlugField(default='default_slug', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='repofolder',
            name='slug',
            field=models.SlugField(default='default_slug', max_length=200),
            preserve_default=False,
        ),
    ]