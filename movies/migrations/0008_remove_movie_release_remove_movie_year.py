# Generated by Django 4.0.8 on 2023-02-22 12:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0007_rename_release_movie_year'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='release',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='year',
        ),
    ]
