# Generated by Django 5.0.7 on 2024-09-01 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_alter_profile_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderhistory',
            name='books',
        ),
        migrations.RemoveField(
            model_name='orderhistory',
            name='user_profile',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='location',
        ),
        migrations.AlterField(
            model_name='profile',
            name='invite_code',
            field=models.CharField(max_length=100),
        ),
        migrations.DeleteModel(
            name='Address',
        ),
        migrations.DeleteModel(
            name='OrderHistory',
        ),
    ]
