# Generated by Django 5.1.4 on 2025-01-07 06:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common_app', '0003_alter_driver_user_id_company'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Driver',
        ),
    ]
