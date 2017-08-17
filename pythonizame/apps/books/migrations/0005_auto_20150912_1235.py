# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor_uploader.fields


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_auto_20150912_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(max_length=20000),
        ),
    ]
