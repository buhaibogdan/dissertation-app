from conf.conf import SMTP_PORT, SMTP_SERVER, SMTP_USERNAME, SMTP_PASSWORD, SMTP_SYSTEM_SENDER
import smtplib
from Services.Log.LogService import logService


class EmailService(object):
    def __init__(self):
        self.instance = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        self.contentType = 'text/html'
        self.fromAddress = SMTP_SYSTEM_SENDER
        self.subject = '-IssueManager-'

    def setTo(self, to):
        self.to = to

    def setFrom(self, address):
        self.fromAddress = address

    def setSubject(self, subject):
        self.subject = subject

    def setContentType(self, contentType):
        self.contentType = contentType

    def setBody(self, body):
        self.body = body

    def send(self):
        self.instance.ehlo()
        self.instance.starttls()
        self.instance.ehlo
        self.instance.login(SMTP_USERNAME, SMTP_PASSWORD)
        try:
            self.instance.sendmail(
                self.fromAddress,
                self.to,
                self._getHeaders() + "\r\n\r\n" + self.body)
        except AttributeError as err:
            logService.log_error("Could not send email. Essential attribute missing: " + err.message)

    def _getHeaders(self):
        headers = [
            "From: " + self.fromAddress,
            "Subject: " + self.subject,
            "To: " + self.to,
            "MIME-Version: 1.0",
            "Content-Type: " + self.contentType
        ]
        return "\r\n".join(headers)