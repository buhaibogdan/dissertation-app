import tornado.websocket
import json
import requests
from Services.History.HistoryService import HistoryService
from conf.conf import webServicesAddress
import tornado
import tornado.web
import tornado.gen


class BaseAsyncHandler(tornado.websocket.WebSocketHandler):
    @property
    def historyService(self):
        return HistoryService()


class HistoryHandler(BaseAsyncHandler):
    def open(self):
        self.getAllHistory()

    def on_message(self, message):
        self.getAllHistory(True)

    def on_close(self):
        self.write_message('no close')

    @tornado.web.asynchronous
    @tornado.gen.engine
    def getAllHistory(self, justNew=False):
        client = tornado.httpclient.AsyncHTTPClient()
        response = yield tornado.gen.Task(client.fetch, webServicesAddress['event'])
        if justNew:
            eventsString = self.getNewHistoryEvents(response.body)
        else:
            eventsString = response.body
            self.initialEvents = eventsString

        self.write_message(eventsString)
        self.finish()

    def getNewHistoryEvents(self, historyString):
        historyJson = json.loads(historyString)
        newHistoryEvents = [event for event in historyJson if event not in self.initialEvents]
        return json.dumps(newHistoryEvents)


class UserHistoryHandler(BaseAsyncHandler):
    def open(self, uid):
        self.uid = uid
        self.getUserHistory(uid)

    def on_message(self, message):
        if message == 'refresh':
            self.getUserHistory(self.uid)

    def on_close(self):
        pass

    @tornado.web.asynchronous
    @tornado.gen.engine
    def getUserHistory(self, uid):
        client = tornado.httpclient.AsyncHTTPClient()
        response = yield tornado.gen.Task(client.fetch, webServicesAddress['event'] + 'user/' + uid)
        self.write_message(response.body)
        self.finish()


class ProjectHistoryHandler(BaseAsyncHandler):
    def open(self, pid):
        self.pid = pid
        self.getProjectHistory(pid)

    def on_message(self, message):
        if message == 'refresh':
            self.getUserHistory(self.pid)

    def on_close(self):
        pass

    @tornado.web.asynchronous
    @tornado.gen.engine
    def getProjectHistory(self, pid):
        client = tornado.httpclient.AsyncHTTPClient()
        response = yield tornado.gen.Task(client.fetch, webServicesAddress['event'] + 'project/' + pid)
        self.write_message(response.body)
        self.finish()