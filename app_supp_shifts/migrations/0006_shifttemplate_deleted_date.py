# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-18 14:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_supp_shifts', '0005_auto_20170618_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='shifttemplate',
            name='deleted_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
