# Generated by Django 3.0.5 on 2021-04-09 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repositories', '0005_auto_20210403_1531'),
        ('issues', '0015_auto_20210409_0844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='associated_file',
            field=models.ForeignKey(blank=True, max_length=100, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='repofile', to='repositories.RepoFile'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='associated_folder',
            field=models.ForeignKey(blank=True, max_length=100, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='repofolder', to='repositories.RepoFolder'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='associated_loc',
            field=models.ForeignKey(blank=True, max_length=100, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='issue_loc', to='repositories.RepoFolder'),
        ),
    ]