# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
#import django_pgjson.fields
import django.contrib.postgres.fields.jsonb
from django.conf import settings
import pythonizame.apps.account.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Power',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, help_text='Superpoder')),
                ('description', models.TextField(null=True, blank=True, max_length=200)),
                ('image', models.ImageField(upload_to=pythonizame.apps.account.models.Power.image_path)),
                ('python_auxiliary', models.BooleanField(help_text='Es una tecnología Auxiliar a Python?', default=False)),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Poderes Python',
                'verbose_name': 'Poder Python',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to=pythonizame.apps.account.models.image_user_profile_path, blank=True)),
                ('cover_image', models.ImageField(null=True, upload_to=pythonizame.apps.account.models.image_user_profile_path, blank=True)),
                ('birthday', models.DateField(null=True, blank=True)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(help_text='Información adicional', null=True, blank=True)),
                ('powers', models.ManyToManyField(to='account.Power', help_text='Super poderes del usuario')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Perfiles de Usuarios',
                'verbose_name': 'Perfil de Usuario',
            },
        ),
    ]
