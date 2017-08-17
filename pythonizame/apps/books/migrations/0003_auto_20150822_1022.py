# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20150822_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='publication_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='book',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=False,
        ),
    ]
