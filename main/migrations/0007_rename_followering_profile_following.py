# Generated by Django 4.1.3 on 2023-02-09 00:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_music_share_to_profile_followering_profile_followers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='followering',
            new_name='following',
        ),
    ]
