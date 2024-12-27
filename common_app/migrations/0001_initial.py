# Generated by Django 5.1.4 on 2024-12-27 05:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('phone_no', models.CharField(max_length=15, unique=True)),
                ('gender', models.CharField(choices=[('male', 'male'), ('other', 'other'), ('female', 'female')], max_length=50)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('profile_url', models.URLField(blank=True, null=True)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('password', models.CharField(max_length=255)),
                ('role', models.CharField(choices=[('user', 'user'), ('driver', 'driver'), ('travel_admin', 'travel_admin'), ('package_admin', 'package_admin'), ('travel_sub_admin', 'travel_sub_admin'), ('package_sub_admin', 'package_sub_admin')], default='user', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('creator_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_users', to='common_app.user')),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='User_Address',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('pin_code', models.CharField(blank=True, max_length=20, null=True)),
                ('street_address', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_id', to='common_app.user')),
            ],
            options={
                'db_table': 'user_address',
            },
        ),
    ]
