# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author_image',
            field=models.CharField(blank=True, max_length=500, null=True, help_text='Llenar si la imagen requiere referencia de su autor'),
        ),
        migrations.AddField(
            model_name='post',
            name='author_link',
            field=models.URLField(blank=True, max_length=10000, null=True, help_text='URL de referencia al autor.'),
        ),
    ]
