# Generated by Django 5.1.4 on 2025-01-21 09:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common_app', '0023_rename_package_necessities_id_bidproposal_bid_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bidproposal',
            name='bid_status',
        ),
    ]
