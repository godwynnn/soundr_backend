# Generated by Django 4.1.3 on 2023-02-15 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_userpackage_txref'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpackage',
            name='ps_txref',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
