import tornado.websocket
import json
from Services.History.HistoryService import HistoryService
from conf.conf import webServicesAddress
import tornado
import tornado.web
import tornado.gen


class BaseAsyncHandler(tornado.websocket.WebSocketHandler):
    @property
    def historyService(self):
        return HistoryService()

    def getNewHistoryEvents(self, historyString):

        historyJson = json.loads(historyString)
        try:
            newHistoryEvents = [event for event in historyJson if event not in self.initialEvents]
            #keep for next call
            self.initialEvents = newHistoryEvents + historyJson
        except AttributeError:
            return ''
        return json.dumps(newHistoryEvents)


class HistoryHandler(BaseAsyncHandler):
    def open(self):
        self.getAllHistory()

    def on_message(self, message):
        self.getAllHistory(True)

    def on_close(self):
        self.write_message('closed')

    @tornado.web.asynchronous
    @tornado.gen.engine
    def getAllHistory(self, justNew=False):
        client = tornado.httpclient.AsyncHTTPClient()
        response = yield tornado.gen.Task(client.fetch, webServicesAddress['event'])
        if justNew:
            eventsString = self.getNewHistoryEvents(response.body)
        else:
            eventsString = response.body
            self.initialEvents = json.loads(eventsString)

        self.write_message(eventsString)
        self.finish()


class UserHistoryHandler(BaseAsyncHandler):
    def open(self, uid):
        self.uid = uid
        self.getUserHistory(uid)

    def on_message(self, message):
        self.getUserHistory(self.uid, True)

    def on_close(self):
        self.write_message('closed')

    @tornado.web.asynchronous
    @tornado.gen.engine
    def getUserHistory(self, uid, justNew=False):
        client = tornado.httpclient.AsyncHTTPClient()
        response = yield tornado.gen.Task(client.fetch, webServicesAddress['event'] + 'user/' + uid)

        if justNew:
            eventsString = self.getNewHistoryEvents(response.body)
        else:
            eventsString = response.body
            self.initialEvents = json.loads(eventsString)
        self.write_message(eventsString)
        self.finish()


class ProjectHistoryHandler(BaseAsyncHandler):
    def open(self, pid):
        self.pid = pid
        self.getProjectHistory(pid)

    def on_message(self, message):
        self.getProjectHistory(self.pid, True)

    def on_close(self):
        pass

    @tornado.web.asynchronous
    @tornado.gen.engine
    def getProjectHistory(self, pid, justNew=False):
        client = tornado.httpclient.AsyncHTTPClient()
        response = yield tornado.gen.Task(client.fetch, webServicesAddress['event'] + 'project/' + pid)
        if justNew:
            eventsString = self.getNewHistoryEvents(response.body)
        else:
            eventsString = response.body
            self.initialEvents = json.loads(eventsString)

        self.write_message(eventsString)
        self.finish()