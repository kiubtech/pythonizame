# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.CharField(help_text='Autor del libro', max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='book',
            name='url',
            field=models.URLField(help_text='Url de la fuente donde se consulta la información', max_length=800),
        ),
    ]
