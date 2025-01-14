# Generated by Django 5.1.4 on 2025-01-13 07:06

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common_app', '0011_alter_userpermission_granted_by_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TourPackageBid',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('tour_package_id', models.UUIDField()),
                ('transport_vehicle_id', models.UUIDField()),
                ('bid_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bid_status', models.CharField(choices=[('pending', 'pending'), ('bidded', 'bidded'), ('accepted', 'accepted'), ('rejected', 'rejected')], default='pending', max_length=15)),
                ('additional_info', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'tour_package_bids',
            },
        ),
    ]
