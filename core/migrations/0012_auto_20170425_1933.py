# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-04-25 19:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20170425_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visualisation',
            name='interior_arc_percent',
            field=models.IntegerField(default=40),
        ),
    ]