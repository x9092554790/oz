# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-23 11:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quest', '0012_quest_is_partner'),
    ]

    operations = [
        migrations.AddField(
            model_name='quest',
            name='address',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='quest',
            name='phone',
            field=models.CharField(max_length=255, null=True),
        ),
    ]