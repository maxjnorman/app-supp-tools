# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-18 16:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_supp_teams', '0004_auto_20170618_1524'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='manager_group_name',
        ),
    ]