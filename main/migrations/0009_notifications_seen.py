# Generated by Django 4.1.3 on 2023-02-09 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_notifications'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='seen',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]