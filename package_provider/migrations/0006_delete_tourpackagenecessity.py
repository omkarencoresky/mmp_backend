# Generated by Django 5.1.4 on 2025-01-17 06:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('package_provider', '0005_remove_tourpackagenecessity_vehicle_type_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TourPackageNecessity',
        ),
    ]
