# Generated by Django 3.2 on 2022-10-14 18:24

import classroom.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institution', models.CharField(max_length=200)),
                ('department', models.CharField(max_length=200)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profiles/dp/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.CharField(default=classroom.models.Classroom.get_uuid, editable=False, max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('students', models.ManyToManyField(related_name='student', to='classroom.Account')),
                ('teachers', models.ManyToManyField(related_name='teacher', to='classroom.Account')),
            ],
        ),
        migrations.CreateModel(
            name='ClassroomPost',
            fields=[
                ('id', models.CharField(default=classroom.models.ClassroomPost.get_uuid, editable=False, max_length=50, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=9999)),
                ('posted', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.account')),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.classroom')),
            ],
        ),
    ]
