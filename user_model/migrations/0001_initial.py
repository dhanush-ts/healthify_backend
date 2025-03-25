# Generated by Django 5.1.7 on 2025-03-25 08:31

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
                ('full_name', models.CharField(max_length=30, unique=True)),
                ('password', models.CharField(blank=True, default='Changeme@123', max_length=20)),
                ('phone_number', models.CharField(default='0000000000', max_length=10)),
                ('dob', models.DateField()),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=10)),
                ('height', models.CharField(max_length=10)),
                ('weight', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=255)),
                ('medical_history', models.TextField(blank=True, null=True)),
                ('genetic_predisposition', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
