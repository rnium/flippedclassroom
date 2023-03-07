# Generated by Django 3.2 on 2023-03-07 06:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20230224_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profiles/dp/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['.jpg', '.jpeg', '.png'])]),
        ),
    ]