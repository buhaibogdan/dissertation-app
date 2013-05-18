from HistoryEntity import HistoryEntity
from HistoryDAO import HistoryDAO
import pika
import json


class HistoryService(object):

    def __init__(self, dao=None):
        if dao is None:
            self.__DAO = HistoryDAO()
        self.initAMQP()

    def initAMQP(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='history', type='topic')
        self.channel.queue_declare(queue='history_queue')

    def getHistory(self):
        return self.__DAO.getHistory()

    def getUserHistory(self, uid):
        return self.__DAO.getUserHistory(uid)

    def getProjectHistory(self, pid):
        return self.__DAO.getProjectHistory(pid)

    def updateHistory(self, uid, pid, event_id, message):
        hEvent = json.dumps({
            'uid': uid,
            'pid': pid,
            'event_id': event_id,
            'message': message
        })

        self.channel.basic_publish(exchange='history',
                                   routing_key='history.events',
                                   body=hEvent)

        print " [x] Sent %r" % hEvent

    def convertToEntity(self, historyJson):
        h = json.loads(historyJson)
        try:
            hEvent = HistoryEntity(h['uid'], h['pid'], h['event_id'], h['message'])
            return hEvent
        except KeyError:
            return False

    def convertToJson(self, recordList):
        jsonHistory = []
        try:
            for h in recordList:
                jsonHistory.append({
                    'id': h.id,
                    'uid': h.uid,
                    'username': h.user.username,
                    'pid': h.pid,
                    'project': h.project.title,
                    'event_id': h.event_id,
                    'event': h.event.name,
                    'message': h.message
                })
        except AttributeError:
            return '' #TODO: logger

        return json.dumps(jsonHistory)

    def sendEmails(self, uid, pid, message):
        #sendEmails uses just for demonstration purposes AMQP (topics)
        #normaly we would just insert emails in a DB and have something that
        #queries the DB and sends emails
        fromAddress = 'system'
        toAddress = 'all' #get user preferences, list of emails
        body = message
        emailDetails = json.dumps({
            'from': fromAddress,
            'to': toAddress,
            'body': body
        })

        self.channel.basic_publish(exchange='history',
                                   routing_key='history.emails',
                                   body=emailDetails)

    def __del__(self):
        try:
            self.connection.close()
        except AttributeError:
            # connection was not opened
            return