import pika
import sys
sys.path.append('/home/bb/PycharmProjects/dissertation-app')
from Services.Report.ReportService import ReportService

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))

channel = connection.channel()
channel.queue_declare(queue='rpc_queue')


def on_request(ch, method, props, body):
    pid = int(body)

    print " [!] Generating report for project with pid =%s"  % (pid,)
    service = ReportService()
    response = service.createReportForProject(pid)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=response)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')

print " [*] Awaiting report requests."
channel.start_consuming()