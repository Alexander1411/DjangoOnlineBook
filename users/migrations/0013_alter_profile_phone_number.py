# Generated by Django 5.0.7 on 2024-08-07 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_profile_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(default='+353000000000', max_length=15, unique=True),
        ),
    ]
