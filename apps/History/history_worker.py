import sys
sys.path.append('/home/bb/PycharmProjects/dissertation-app')
import pika
import json
from Services.History.HistoryDAO import HistoryDAO
from Services.History.HistoryService import HistoryService
from Services.Log.LogService import LogService

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='history', type='topic')

binding_keys = sys.argv[1:]
if not binding_keys:
    print >> sys.stderr, "Usage: %s [binding_key]..." % (sys.argv[0],)
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(exchange='history',
                       queue='history_queue',
                       routing_key=binding_key)

print ' [*] Waiting for events to fire. To cancel press CTRL+C'

hService = HistoryService()
logService = LogService()


def callback(ch, method, properties, body):
    print " [x] Received %r wih key %r" % (body, method.routing_key)
    hEvent = hService.convertToEntity(body)
    if method.routing_key == 'history.events':
        if hEvent:
            dao = HistoryDAO()
            dao.updateHistory(hEvent)
            print " [x] Saved."
        else:
            print "Nothing to save. Invalid object passed."
            logService.log_info("[HISTORY-WORKER] Nothing to save. Invalid object passed.")
    elif method.routing_key == 'history.emails':
        try:
            emailInfo = json.loads(body)
            print " [x] Sent email to %r, from %r, with message:  %r " \
                  % (emailInfo['to'], emailInfo['from'], emailInfo['from'])
        except KeyError:
            print "Not enough info to compose email."
            logService.log_info("[HISTORY-WORKER] Not enough info to compose email.")

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue='history_queue')

channel.start_consuming()