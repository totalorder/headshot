# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0011_monitor_environment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='status',
            name='monitor'
        ),
        migrations.AddField(
            model_name='status',
            name='monitor',
            field=models.ForeignKey(related_name=b'statuses', to='monitor.Monitor')
        ),
    ]
