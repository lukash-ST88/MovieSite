# Generated by Django 4.0.8 on 2023-02-22 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0008_remove_movie_release_remove_movie_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='year',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Год'),
        ),
    ]
