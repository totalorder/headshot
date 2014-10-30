# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0006_auto_20141029_1437'),
    ]

    operations = [
        migrations.RunSQL("ALTER TABLE monitor_monitor ALTER COLUMN id SET default nextval('monitor_monitor_id_seq'::regclass)")
    ]
