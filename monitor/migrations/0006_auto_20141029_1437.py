# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0005_urlmonitor'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitor',
            name='interval',
            field=models.IntegerField(default=10),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='monitor',
            name='id'
        ),
        migrations.AddField(
            model_name='monitor',
            name='id',
            field=models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
        ),
    ]
