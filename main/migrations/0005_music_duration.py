# Generated by Django 4.1.3 on 2022-12-27 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_music_artist_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='music',
            name='duration',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]