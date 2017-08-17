# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import pythonizame.apps.account.models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20150801_1258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achievement',
            name='image',
            field=models.ImageField(upload_to=pythonizame.apps.account.models.Achievement.image_path),
        ),
    ]
