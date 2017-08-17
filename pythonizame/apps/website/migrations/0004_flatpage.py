# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-30 05:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flatpages', '0001_initial'),
        ('website', '0003_auto_20161029_2238'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlatPage',
            fields=[
                ('flatpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='flatpages.FlatPage')),
                ('status', models.IntegerField(choices=[(0, 'Oculto'), (1, 'Visible')], default=1, help_text='¿Define si es oculto o visible?')),
            ],
            bases=('flatpages.flatpage',),
        ),
    ]
