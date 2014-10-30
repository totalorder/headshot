# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0009_localprocessmonitor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='localprocessmonitor',
            name='id',
        ),
        migrations.RemoveField(
            model_name='localprocessmonitor',
            name='monitor',
        ),
        migrations.RemoveField(
            model_name='urlmonitor',
            name='id',
        ),
        migrations.RemoveField(
            model_name='urlmonitor',
            name='monitor',
        ),
        migrations.AddField(
            model_name='localprocessmonitor',
            name='monitor_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=-1, serialize=False, to='monitor.Monitor'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='urlmonitor',
            name='monitor_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=-1, serialize=False, to='monitor.Monitor'),
            preserve_default=False,
        ),
    ]
