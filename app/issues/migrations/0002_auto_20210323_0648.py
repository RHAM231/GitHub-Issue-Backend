# Generated by Django 3.0.5 on 2021-03-23 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='closded_at',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='updated_at',
            field=models.DateTimeField(blank=True),
        ),
    ]