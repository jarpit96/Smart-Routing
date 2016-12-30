# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-26 19:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routing', '0002_locality_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locality',
            name='crime_wt',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='locality',
            name='poi_wt',
            field=models.FloatField(default=3),
        ),
        migrations.AlterField(
            model_name='locality',
            name='traffic_wt',
            field=models.FloatField(default=3),
        ),
    ]
