# Generated by Django 3.2 on 2022-12-28 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weeklies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inclasstutorial',
            name='description',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='postclasstutorial',
            name='description',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='preclasstutorial',
            name='description',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='weekly',
            name='in_class_instruction',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='weekly',
            name='post_class_instruction',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='weekly',
            name='pre_class_instruction',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]
