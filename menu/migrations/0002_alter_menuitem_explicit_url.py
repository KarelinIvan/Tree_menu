# Generated by Django 5.2 on 2025-04-25 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='explicit_url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
