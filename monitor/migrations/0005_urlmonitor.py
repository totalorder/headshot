# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0004_auto_20141022_0652'),
    ]

    operations = [
        migrations.CreateModel(
            name='URLMonitor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=4096)),
                ('warn_latency', models.IntegerField()),
                ('monitor', models.ForeignKey(to='monitor.Monitor')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
