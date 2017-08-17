# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20150801_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='achievement',
            name='message_for_user',
            field=models.TextField(help_text='Mensaje que aparecerá al usuario', default='felicidades', max_length=400),
            preserve_default=False,
        ),
    ]
