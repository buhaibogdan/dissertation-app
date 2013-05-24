import pika
from LogDB import logDB


class LogService(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='direct_logs',
                                      type='direct')

    def log_error(self, message):
        self.__log__('error', message)

    def log_warning(self, message):
        self.__log__('warning', message)

    def log_info(self, message):
        self.__log__('info', message)

    def __log__(self, severity, message):
        print " [x] Sent %r: - %r" % (severity, message)
        self.channel.basic_publish(exchange='direct_logs',
                                   routing_key=severity,
                                   body=message)

    def __del__(self):
        self.connection.close()

    def log_error_db(self, message):
        logDB.insertError(message)

    def log_warning_db(self, message):
        logDB.insertWarning(message)

    def log_notice_db(self, message):
        logDB.insertNotice(message)

    def getErrors(self, startDate=None, endDate=None):
        errors = logDB.getErrors()
        return errors

    def getWarnings(self, startDate=None, endDate=None):
        warnings = logDB.getWarnings()
        return warnings

    def getNotices(self, startDate=None, endDate=None):
        notices = logDB.getNotices()
        return notices


logService = LogService()