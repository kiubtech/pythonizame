# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import pythonizame.apps.books.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=800)),
                ('slug', models.SlugField(max_length=1000, unique=True)),
                ('image', models.ImageField(help_text='Imagen de Portada', null=True, upload_to=pythonizame.apps.books.models.image_path_book, blank=True, max_length=1000)),
                ('file', models.FileField(null=True, upload_to=pythonizame.apps.books.models.file_path_book, blank=True, max_length=1000)),
                ('description', models.TextField(max_length=2000)),
                ('url', models.URLField(max_length=800, help_text='Url de la fuente')),
                ('published', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Libros',
                'verbose_name': 'Libro',
            },
        ),
        migrations.CreateModel(
            name='BookCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('slug', models.SlugField(max_length=600)),
            ],
            options={
                'verbose_name_plural': 'Categorías de Libros',
                'verbose_name': 'Categoría de Libro',
            },
        ),
        migrations.CreateModel(
            name='TagBook',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('slug', models.SlugField(max_length=1000)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Tags de Libros',
                'verbose_name': 'Tag de Libro',
            },
        ),
        migrations.AddField(
            model_name='book',
            name='categories',
            field=models.ManyToManyField(to='books.BookCategory'),
        ),
        migrations.AddField(
            model_name='book',
            name='created_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='book',
            name='tags',
            field=models.ManyToManyField(to='books.TagBook', blank=True),
        ),
    ]
