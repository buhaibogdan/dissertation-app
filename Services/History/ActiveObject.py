import threading
import requests
from Services.Log.LogService import logService


class ActiveObject(threading.Thread):
    def __init__(self, uid):
        threading.Thread.__init__(self)
        self._finished = threading.Event()
        self._interval = 120

        self.uid = uid
        self.historyAll = ''
        self.historyUser = ''

    def setInterval(self, interval):
        self._interval = interval

    def stop(self):
        """ stop the thread """
        self._finished.set()

    def run(self):
        while True:
            if self._finished.isSet():
                return
            self.task()
            self._finished.wait(self._interval)

    def task(self):
        try:
            self.historyAll = requests.get('http://localhost:8001/').content
        except requests.ConnectionError:
            logService.log_error('[HistoryService] ActiveObject could not connect to EventWebService')