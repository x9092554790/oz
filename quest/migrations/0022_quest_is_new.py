# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-04-17 07:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quest', '0021_quest_title_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='quest',
            name='is_new',
            field=models.BooleanField(default=False),
        ),
    ]
