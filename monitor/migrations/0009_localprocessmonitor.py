# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0008_urlmonitor_foreignint'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocalProcessMonitor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('command', models.TextField()),
                ('success_message', models.CharField(max_length=128)),
                ('monitor', models.ForeignKey(to='monitor.Monitor')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
