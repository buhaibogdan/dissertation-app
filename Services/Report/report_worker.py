import pika
import sys
sys.path.append('/home/bb/PycharmProjects/dissertation-app')
from Services.Report.ReportService import ReportService
from Services.Utils.EmailService import EmailService

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))

channel = connection.channel()
channel.queue_declare(queue='report_queue', durable=True)


def on_request(ch, method, props, body):
    pid = int(body)

    print " [!] Generating pdf report for project with pid = %s" % (pid,)
    service = ReportService()
    service.createReportForProjectPDF(pid)
    print " [!] Sending email with report as attachment..."
    emailService = EmailService()
    emailService.setTo("buhaibogdan@yahoo.com")
    emailService.setBody("just some text for test here")
    emailService.setSubject("Test")
    emailService.attachProject(pid)
    emailService.send()
    print " [.] Done."
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='report_queue')

print " [*] Awaiting report requests."
channel.start_consuming()