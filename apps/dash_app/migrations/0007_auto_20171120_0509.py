# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-11-20 05:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dash_app', '0006_auto_20171120_0503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='commentor',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments_posted', to='dash_app.User'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='message',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='dash_app.Message'),
        ),
        migrations.AlterField(
            model_name='message',
            name='poster',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages_posted', to='dash_app.User'),
        ),
        migrations.AlterField(
            model_name='message',
            name='receiver',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages_received', to='dash_app.User'),
        ),
    ]
