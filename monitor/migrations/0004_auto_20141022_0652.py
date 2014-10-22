# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0003_status_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitor',
            name='image',
            field=models.TextField(default=b'front/images/db.gif'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='status',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
