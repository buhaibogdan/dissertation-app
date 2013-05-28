from conf.conf import SMTP_PORT, SMTP_SERVER, SMTP_USERNAME, SMTP_PASSWORD, SMTP_SYSTEM_SENDER
import smtplib
from Services.Log.LogService import logService
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from email.mime.application import MIMEApplication

class EmailService(object):
    def __init__(self):
        self.instance = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        self.contentType = 'text/html'
        self.fromAddress = SMTP_SYSTEM_SENDER
        self.subject = '-IssueManager-'
        self.msg = None

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

    def _getHeaders(self):
        headers = [
            "From: " + self.fromAddress,
            "Subject: " + self.subject,
            "To: " + self.to,
            "MIME-Version: 1.0",
            "Content-Type: " + self.contentType
        ]
        return "\r\n".join(headers)

    def attachProject(self, pid):
        self.msg = MIMEMultipart()
        self.msg['Subject'] = 'Report for project'
        self.msg['From'] = 'buhaibogdan@gmail.com'
        self.msg['Reply-to'] = 'buhaibogdan@gmail.com'
        self.msg['To'] = 'buhaibogdan@yahoo.com'

        # This is the textual part:
        part = MIMEText("Hello, \r\n This is a system generated report as requested. "
                        "If you did not request it, please ignore it. \r\n IssueManager System")
        self.msg.attach(part)

        # This is the binary part(The Attachment):
        part = MIMEApplication(open("/home/bb/PycharmProjects/dissertation-app/Services/Report/" +
                                    "generated_reports/project_1_report.pdf", "rb").read())
        part.add_header('Content-Disposition', 'attachment', filename="report_project_1.pdf")
        self.msg.attach(part)

    def send(self):
        self.instance.ehlo()
        self.instance.starttls()
        self.instance.ehlo
        self.instance.login(SMTP_USERNAME, SMTP_PASSWORD)

        if self.msg is None:
            msg = self._getHeaders() + "\r\n\r\n" + self.body
        else:
            msg = self.msg.as_string()
        try:
            self.instance.sendmail(
                self.fromAddress,
                self.to,
                msg)
        except AttributeError as err:
            logService.log_error("Could not send email. Essential attribute missing: " + err.message)


"""

mailer.sendmail(from_, to, msg.as_string())
mailer.close()
"""