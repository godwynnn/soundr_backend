# Generated by Django 4.1.3 on 2022-12-27 00:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_music_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='music',
            name='duration',
        ),
    ]
