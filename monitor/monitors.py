# coding=utf-8
import logging
import threading
import time
import traceback
import requests
from monitor import oracle
from monitor.models import Monitor, Status


class MonitorWorker(threading.Thread):
    def __init__(self, name, image, interval=10):
        super(MonitorWorker, self).__init__()

        self.name = name
        self.interval = interval
        self.image = image

        try:
            self.monitor = Monitor.objects.get(pk=self.name)
        except Monitor.DoesNotExist:
            self.monitor = Monitor.objects.create(pk=self.name,
                                                  type=self.__class__.__name__,
                                                  description=self.getDescription(),
                                                  image=self.image)

    def getDescription(self):
        raise NotImplementedError()

    def run(self):
        while True:
            try:
                self.work()
            except:
                logging.exception(u"Error in %s: " % self.__class__.__name__)
            time.sleep(self.interval)

    def work(self):
        raise NotImplementedError()

class DBMonitor(MonitorWorker):
    def __init__(self, name, image, interval=10, dbid='dev'):
        self.dbid = dbid
        super(DBMonitor, self).__init__(name, image, interval)

    def getDescription(self):
        return self.dbid

    def work(self):
        status = Status()
        status.monitor = self.monitor


        try:
            conn = oracle.createDatabaseConnection(self.dbid)
            cur = conn.cursor()
            cur.execute(u"SELECT id FROM item_master WHERE ROWNUM < 10")
            result = cur.fetchall()
            status.code = Status.OK
            status.short_desc = "Good stuff"
        except Exception as e:
            status.code = Status.FAILED
            status.short_desc = unicode(e)[:128]
            status.desc = u"%s\n%s" % (e, traceback.format_exc())
        status.save()




class UrlMonitor(MonitorWorker):
    def __init__(self, name, image, interval=10, url=None, warn_latency=500):
        self.url = url

        super(UrlMonitor, self).__init__(name, image, interval)
        if url is None:
            raise ValueError(u"Url has to be set for UrlMonitor!")
        self.warn_latency = warn_latency

    def getDescription(self):
        return self.url

    def work(self):
        status = Status()
        status.monitor = self.monitor
        try:
            start_time = time.time()
            response = requests.get(self.url)
            if response.status_code == 200:
                latency = int((time.time() - start_time) * 1000)
                if latency >= self.warn_latency:
                    status.code = Status.WARN
                    status.short_desc = u"(200) Latency is %s ms" % latency
                else:
                    status.code = Status.OK
                    status.short_desc = u"(200) OK"
        except requests.HTTPError as e:
            status.code = Status.FAILED
            status.short_desc = unicode(e)[:128]
            status.desc = unicode(e)
        except Exception as e:
            status.code = Status.FAILED
            status.short_desc = unicode(e)[:128]
            status.desc = u"%s\n%s" % (e, traceback.format_exc())
        status.save()


def getMonitors():
    return (
        UrlMonitor(u"Localhost", url=u"http://localhost:8000/", image="front/images/server.png"),
        UrlMonitor(u"AIM Web: prd", url=u"http://prd.aim.deadlock.se:9000/", image="front/images/server.png"),
        DBMonitor(u"AIM DB: dev", dbid="dev", image="front/images/db.gif"),
    )
