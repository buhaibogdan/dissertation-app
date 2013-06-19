from MySQLdb.constants.ER import NOT_SUPPORTED_AUTH_MODE
import tornado.websocket
import json
from Services.History.HistoryService import HistoryService
from conf.conf import webServicesAddress, webServicesAccounts
import tornado
import tornado.web
import tornado.gen
from tornado.httpclient import HTTPRequest
from Services.Log.LogService import logService


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

    def check_status(self, code):
        if code == 403 or code == 401:
            logService.log_error('[History] Could not authenticate to EventWebService to get all history')
            self.write_message(json.dumps({'error': '1'}))
            self.finish()


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
        request = tornado.httpclient.HTTPRequest(
            webServicesAddress['event'],
            validate_cert=False,
            auth_username=webServicesAccounts['event'][0],
            auth_password=webServicesAccounts['event'][1],
            auth_mode='basic')
        response = yield tornado.gen.Task(client.fetch, request)
        self.check_status(response.code)

        if justNew:
            eventsString = self.getNewHistoryEvents(response.body)
        else:
            eventsString = response.body
            self.initialEvents = json.loads(eventsString)

        self.write_message(eventsString)
        self.finish()


class UserHistoryHandler(BaseAsyncHandler):
    def initialize(self):
        pass

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
        request = tornado.httpclient.HTTPRequest(
            webServicesAddress['event'] + 'user/' + uid,
            validate_cert=False,
            auth_username=webServicesAccounts['event'][0],
            auth_password=webServicesAccounts['event'][1],
            auth_mode='basic')
        response = yield tornado.gen.Task(client.fetch, request)
        self.check_status(response.code)

        if justNew:
            eventsString = self.getNewHistoryEvents(response.body)
        else:
            eventsString = response.body
            self.initialEvents = json.loads(eventsString)
        self.write_message(eventsString)
        self.finish()


class ProjectHistoryHandler(BaseAsyncHandler):
    def initialize(self):
        pass

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
        request = tornado.httpclient.HTTPRequest(
            webServicesAddress['event'] + 'project/' + pid,
            validate_cert=False,
            auth_username=webServicesAccounts['event'][0],
            auth_password='c',
            auth_mode='basic')

        response = yield tornado.gen.Task(client.fetch, request)
        self.check_status(response.code)
        if justNew:
            eventsString = self.getNewHistoryEvents(response.body)
        else:
            eventsString = response.body
            self.initialEvents = json.loads(eventsString)
        self.write_message(eventsString)

        self.finish()