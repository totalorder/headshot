# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Monitor',
            fields=[
                ('id', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('type', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=32, choices=[(b'OK', b'OK'), (b'Warn', b'Warn'), (b'Failed', b'Failed'), (b'Invalid', b'Invalid')])),
                ('short_desc', models.CharField(max_length=128)),
                ('desc', models.TextField()),
                ('monitor', models.ForeignKey(related_name=b'statuses', to='monitor.Monitor')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
