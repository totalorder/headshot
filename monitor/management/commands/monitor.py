# coding=utf-8
from __future__ import absolute_import
import logging
from django.core.management.base import BaseCommand
from monitor.monitors import getMonitors

logger = logging.getLogger("console")


class Command(BaseCommand):
    help = 'Starts monitoring'

    def handle(self, *args, **options):
        logger.info(u"Initializing monitors...")
        monitors = getMonitors()
        for monitor in monitors:
            monitor.daemon = True
        logger.info(u"Starting monitors...")
        [monitor.start() for monitor in monitors]
        logger.info(u"Monitors are running!")
        try:
            while 1:
                [monitor.join(0.5) for monitor in monitors]
        except KeyboardInterrupt:
            logger.info(u"Shutting down...")



