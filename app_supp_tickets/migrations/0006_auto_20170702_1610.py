# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-02 15:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_supp_tickets', '0005_auto_20170702_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='sla_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
