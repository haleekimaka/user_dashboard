# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-11-20 05:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash_app', '0005_auto_20171120_0501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='message',
            name='message',
            field=models.CharField(max_length=255),
        ),
    ]
