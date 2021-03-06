# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-26 13:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quest', '0009_video_quest'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='description',
            field=models.TextField(max_length=4096, null=True),
        ),
        migrations.AddField(
            model_name='page',
            name='title',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='quest',
            name='seo_description',
            field=models.TextField(max_length=4096, null=True),
        ),
        migrations.AddField(
            model_name='quest',
            name='seo_title',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
