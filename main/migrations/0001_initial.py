# Generated by Django 5.0.3 on 2024-04-10 13:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.CharField(max_length=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=24)),
                ('email', models.EmailField(max_length=254)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ApiUsageLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('google_api_calls', models.IntegerField(default=0, null=True)),
                ('unsplash_api_calls', models.IntegerField(default=0, null=True)),
                ('pexels_api_calls', models.IntegerField(default=0, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.session')),
            ],
        ),
        migrations.AddField(
            model_name='session',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.user'),
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gallery', models.CharField(max_length=12)),
                ('stencil_data', models.JSONField()),
                ('image_data', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.session')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.user')),
            ],
        ),
    ]
