# Generated by Django 5.0.7 on 2024-08-15 11:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_alter_profile_phone_number'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
