# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0002_monitor_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime.now),
            preserve_default=True,
        ),
    ]
