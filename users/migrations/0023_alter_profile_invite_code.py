# Generated by Django 5.0.7 on 2024-09-01 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_remove_orderhistory_books_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='invite_code',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
