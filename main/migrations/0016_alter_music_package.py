# Generated by Django 4.1.3 on 2023-02-15 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_userpackage_ps_txref'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='package',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.userpackage'),
        ),
    ]
