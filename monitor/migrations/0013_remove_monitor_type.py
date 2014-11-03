# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0012_remake_status_fk'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monitor',
            name='type',
        ),
    ]
