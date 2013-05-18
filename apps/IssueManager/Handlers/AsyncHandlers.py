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
        pass

    def on_close(self):
        self.write_message('no close')

    @tornado.web.asynchronous
    @tornado.gen.engine
    def getAllHistory(self):
        client = tornado.httpclient.AsyncHTTPClient()
        response = yield tornado.gen.Task(client.fetch, webServicesAddress['event'])
        self.write_message(response.body)
        self.finish()


class UserHistoryHandler(BaseAsyncHandler):
    def open(self, uid):
        self.getUserHistory(uid)

    def on_message(self, message):
        pass

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
        self.getProjectHistory(pid)

    def on_message(self, message):
        pass

    def on_close(self):
        pass

    @tornado.web.asynchronous
    @tornado.gen.engine
    def getProjectHistory(self, pid):
        client = tornado.httpclient.AsyncHTTPClient()
        response = yield tornado.gen.Task(client.fetch, webServicesAddress['event'] + 'project/' + pid)
        self.write_message(response.body)
        self.finish()