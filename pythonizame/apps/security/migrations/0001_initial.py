# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import pythonizame.apps.global_functions
from django.conf import settings
import pythonizame.apps.security.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTokens',
            fields=[
                ('token', models.CharField(default=pythonizame.apps.global_functions.get_cleaned_uuid, primary_key=True, editable=False, serialize=False, max_length=100)),
                ('type', models.IntegerField(choices=[(0, 'Activación de cuenta'), (1, 'Cambiar contraseña')], default=0)),
                ('expiration_date', models.DateTimeField(default=pythonizame.apps.security.models.one_day_hence, null=True, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Tokens de seguridad',
                'verbose_name': 'Tokens de seguridad',
            },
        ),
        migrations.AlterUniqueTogether(
            name='usertokens',
            unique_together=set([('user', 'type')]),
        ),
    ]
