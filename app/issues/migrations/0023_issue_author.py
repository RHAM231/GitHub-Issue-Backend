# Generated by Django 3.0.5 on 2021-05-03 14:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_name'),
        ('issues', '0022_auto_20210429_0856'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='author',
            field=models.ForeignKey(default=2, max_length=100, on_delete=django.db.models.deletion.CASCADE, related_name='issue_author', to='users.Profile'),
            preserve_default=False,
        ),
    ]
