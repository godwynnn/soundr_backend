# Generated by Django 4.1.3 on 2023-01-31 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]