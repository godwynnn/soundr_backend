# Generated by Django 4.1.3 on 2023-01-01 15:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0008_music_favourite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='favourite',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]