# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_auto_20150822_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]
