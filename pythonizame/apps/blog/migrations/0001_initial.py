# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import pythonizame.apps.blog.models
import pythonizame.apps.global_functions
import ckeditor_uploader.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('slug', models.SlugField(max_length=600)),
            ],
            options={
                'verbose_name_plural': 'Categorías de Blog',
                'verbose_name': 'Categoría de Blog',
            },
        ),
        migrations.CreateModel(
            name='FavoritePost',
            fields=[
                ('id', models.UUIDField(default=pythonizame.apps.global_functions.get_cleaned_uuid, primary_key=True, editable=False, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Post Favorito',
                'verbose_name': 'Post Favorito',
            },
        ),
        migrations.CreateModel(
            name='LikePost',
            fields=[
                ('id', models.UUIDField(default=pythonizame.apps.global_functions.get_cleaned_uuid, primary_key=True, editable=False, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Likes de Post',
                'verbose_name': 'Like de Post',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('pin_image', models.ImageField(max_length=1000, upload_to=pythonizame.apps.blog.models.image_path_post)),
                ('main_image', models.ImageField(max_length=1000, upload_to=pythonizame.apps.blog.models.image_path_post)),
                ('title', models.CharField(max_length=800)),
                ('slug', models.SlugField(max_length=600, unique=True)),
                ('abstract', models.TextField(max_length=200, help_text='Máximo 200 caracteres. Texto principal de la presentación')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(max_length=1000000)),
                ('published', models.BooleanField(help_text='Activar para hacer visible en la web', default=False)),
                ('publication_date', models.DateTimeField(null=True, blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, help_text='Autor', related_name='autor')),
                ('categories', models.ManyToManyField(to='blog.Category')),
            ],
            options={
                'verbose_name_plural': 'Publicaciones',
                'verbose_name': 'Publicación',
            },
        ),
        migrations.CreateModel(
            name='TagPost',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('slug', models.SlugField(max_length=1000)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Tags de Post',
                'verbose_name': 'Tag de Post',
            },
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(to='blog.TagPost', blank=True),
        ),
        migrations.AddField(
            model_name='likepost',
            name='post',
            field=models.ForeignKey(to='blog.Post'),
        ),
        migrations.AddField(
            model_name='favoritepost',
            name='post',
            field=models.ForeignKey(to='blog.Post'),
        ),
        migrations.AlterUniqueTogether(
            name='likepost',
            unique_together=set([('created_by', 'post')]),
        ),
        migrations.AlterUniqueTogether(
            name='favoritepost',
            unique_together=set([('created_by', 'post')]),
        ),
    ]
