# Generated by Django 3.2 on 2023-01-09 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weeklies', '0004_rename_must_read_preclassfile_must_study'),
    ]

    operations = [
        migrations.AddField(
            model_name='inclassfile',
            name='must_study',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='postclassfile',
            name='must_study',
            field=models.BooleanField(default=False),
        ),
    ]