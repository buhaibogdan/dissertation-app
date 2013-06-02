import tornado.websocket
import json
from Services.History.HistoryService import HistoryService
from conf.conf import webServicesAddress
import tornado
import tornado.web
import tornado.gen


class HistoryHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self):
        client = tornado.httpclient.AsyncHTTPClient()
        #response = yield tornado.gen.Task(client.fetch, webServicesAddress['event'])
        client.fetch(webServicesAddress['event'], callback=self.on_response)

    def on_response(self, response):
        eventsString = response.body
        self.initialEvents = json.loads(eventsString)

        #self.write_message(eventsString)
        self.write(eventsString)
        self.finish()


class HistoryHandlerSync(tornado.web.RequestHandler):
    def get(self):
        client = tornado.httpclient.HTTPClient()
        response = client.fetch(webServicesAddress['event'])
        eventsString = response.body
        self.initialEvents = json.loads(eventsString)

        #self.write_message(eventsString)
        self.write(eventsString)
        self.finish()


