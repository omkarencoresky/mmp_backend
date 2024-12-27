# Generated by Django 5.1.4 on 2024-12-27 13:46

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OAuthApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('client_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('client_secret', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('redirect_uris', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'oauth_application',
            },
        ),
        migrations.CreateModel(
            name='OAuthAccessToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('expires_at', models.DateTimeField()),
                ('scope', models.TextField(default='read write')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common_app.user')),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common_app.oauthapplication')),
            ],
            options={
                'db_table': 'oauth_access_token',
            },
        ),
        migrations.CreateModel(
            name='OAuthRefreshToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('access_token', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='common_app.oauthaccesstoken')),
            ],
            options={
                'db_table': 'oauth_refresh_token',
            },
        ),
    ]