# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-05-22 14:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_visualisation_y_axis_ticks'),
    ]

    operations = [
        migrations.AddField(
            model_name='visualisation',
            name='bubble_maximum',
            field=models.IntegerField(default=20),
        ),
        migrations.AddField(
            model_name='visualisation',
            name='bubble_minimum',
            field=models.IntegerField(default=0),
        ),
    ]
