# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import pythonizame.apps.website.models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteconfiguration',
            name='favicon',
            field=models.ImageField(upload_to=pythonizame.apps.website.models.website_logo, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='siteconfiguration',
            name='logo',
            field=models.ImageField(upload_to=pythonizame.apps.website.models.website_logo, blank=True, null=True),
        ),
    ]
