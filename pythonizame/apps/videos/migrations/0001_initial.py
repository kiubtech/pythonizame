# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-06-14 02:51
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import pythonizame.apps.videos.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('abstract', models.TextField(max_length=5000)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(max_length=1000000)),
                ('cover', models.ImageField(blank=True, null=True, upload_to=pythonizame.apps.videos.models.image_path_video)),
                ('status', models.IntegerField(choices=[(0, 'No aprobado'), (1, 'Aprobado'), (2, 'En revisión')], default=2)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Lista de reproducción',
                'verbose_name_plural': 'Listas de reproducción',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=1)),
                ('title', models.CharField(max_length=500)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(max_length=1000000)),
                ('url', models.URLField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('playlist', models.ForeignKey(help_text='Lista de reproducción al que pertenece el video', on_delete=django.db.models.deletion.CASCADE, to='videos.PlayList')),
            ],
            options={
                'ordering': ('-order',),
                'verbose_name': 'Video',
                'verbose_name_plural': 'Videos',
            },
        ),
        migrations.CreateModel(
            name='VideoCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'Categoría de videos',
                'verbose_name_plural': 'Categorías de videos',
            },
        ),
        migrations.AddField(
            model_name='playlist',
            name='categories',
            field=models.ManyToManyField(help_text='Categorías a la que pertenece', to='videos.VideoCategory'),
        ),
        migrations.AddField(
            model_name='playlist',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
