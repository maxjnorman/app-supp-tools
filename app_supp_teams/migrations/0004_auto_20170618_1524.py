# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-18 14:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_supp_teams', '0003_auto_20170605_1821'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='default_shift_templates',
        ),
        migrations.AddField(
            model_name='team',
            name='deleted_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
