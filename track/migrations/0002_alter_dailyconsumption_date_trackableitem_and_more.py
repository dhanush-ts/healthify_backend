# Generated by Django 5.1.7 on 2025-03-25 21:30

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0001_initial'),
        ('user_model', '0004_user_drinking_user_exercise_hours_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyconsumption',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.CreateModel(
            name='TrackableItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trackable_items', to='user_model.user')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='dailyconsumption',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='dailyconsumption',
            name='track_item',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='consumption_records', to='track.trackableitem'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='dailyconsumption',
            unique_together={('user', 'track_item', 'date')},
        ),
        migrations.RemoveField(
            model_name='dailyconsumption',
            name='track_type',
        ),
    ]
