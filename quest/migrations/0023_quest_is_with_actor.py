# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-08-02 08:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quest', '0022_quest_is_new'),
    ]

    operations = [
        migrations.AddField(
            model_name='quest',
            name='is_with_actor',
            field=models.BooleanField(default=False),
        ),
    ]