# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import pythonizame.apps.website.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteConfiguration',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(max_length=255, default='Nombre del sitio')),
                ('logo', models.ImageField(upload_to=pythonizame.apps.website.models.website_logo)),
            ],
            options={
                'verbose_name': 'Site Configuration',
            },
        ),
    ]
