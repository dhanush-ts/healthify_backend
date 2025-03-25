# Generated by Django 5.1.7 on 2025-03-25 21:25

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_model', '0004_user_drinking_user_exercise_hours_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyConsumption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now, unique=True)),
                ('track_type', models.CharField(max_length=50)),
                ('units', models.PositiveIntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='daily_consumption', to='user_model.user')),
            ],
            options={
                'unique_together': {('user', 'track_type', 'date')},
            },
        ),
    ]
