# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-11 06:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20160311_0100'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='courses',
            table='courses',
        ),
        migrations.AlterModelTable(
            name='prerequisites',
            table='prerequisites',
        ),
        migrations.AlterModelTable(
            name='registered',
            table='registered',
        ),
        migrations.AlterModelTable(
            name='timeslots',
            table='timeslots',
        ),
    ]