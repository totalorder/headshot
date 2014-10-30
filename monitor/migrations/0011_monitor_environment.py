# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0010_auto_20141030_0823'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitor',
            name='environment',
            field=models.CharField(default='dev', max_length=3, choices=[(b'dev', b'dev'), (b'tst', b'tst'), (b'trn', b'trn'), (b'prd', b'prd')]),
            preserve_default=False,
        ),
    ]
