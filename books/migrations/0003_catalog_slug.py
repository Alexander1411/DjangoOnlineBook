# Generated by Django 5.0.7 on 2024-08-13 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_catalog_cover_image_catalog_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='catalog',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
    ]
