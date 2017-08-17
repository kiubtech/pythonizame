# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0002_auto_20150728_0311'),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=400)),
                ('image', models.ImageField(upload_to='')),
                ('description', models.TextField(max_length=400)),
                ('num_available', models.IntegerField(help_text='Limitado a una cantidad de personas. Ej. 100 primeros registros')),
            ],
            options={
                'verbose_name_plural': 'Logros',
                'verbose_name': 'Logro',
            },
        ),
        migrations.CreateModel(
            name='UserAchievement',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('viewed', models.BooleanField(default=False, help_text='Ya lo vio el usuario?')),
                ('date_received', models.DateField()),
                ('achievement', models.ForeignKey(to='account.Achievement')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Logros de usuario',
                'verbose_name': 'Logro de usuario',
            },
        ),
        migrations.AlterUniqueTogether(
            name='userachievement',
            unique_together=set([('achievement', 'user')]),
        ),
    ]
