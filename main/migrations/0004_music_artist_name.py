# Generated by Django 4.1.3 on 2022-12-01 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_music_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='music',
            name='artist_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]