# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0007_monitor_nextval'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='urlmonitor',
            name='monitor'),
        migrations.AddField(
            model_name='urlmonitor',
            name='monitor',
            field=models.ForeignKey(to='monitor.Monitor'))
    ]
