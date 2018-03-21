import smtplib
import os
from Service.Collection import Error
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

USERNAME = os.getenv("EMAIL_USERNAME")
PASSWORD = os.getenv("EMAIL_PASSWORD")
FROMADDR = "reports@servus.io"

if USERNAME is None or PASSWORD is None:
    logging.warning("INVALID USER NAME AND PASSWORD FOR EMAIL")


class MailServer:

    def __enter__(self):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()

        server.starttls()
        server.login(USERNAME, PASSWORD)
        self.server = server

        return server

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server.quit()


def send_error_report(to_addr: str, subject: str, error: Error):
    with MailServer() as server:
        msg = "\r\n".join([
            "From: " + FROMADDR,
            "To: " + to_addr,
            "Subject: " + subject,
            "",
            str(error)
        ])
        logging.info("Sending error report: %s", msg)
        server.sendmail(FROMADDR, to_addr, msg)


def send_metric_report(to_addr: str, subject: str, metrics):
    with MailServer() as server:
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = FROMADDR
        msg['To'] = to_addr

        # Create the body of the message (a plain-text and an HTML version).
        text = metrics.report

        with open("./Service/email_templates/metrics.html") as f:
            html = f.read().format(metrics.node_html(), metrics.report)

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)

        # sendmail function takes 3 arguments: sender's address, recipient's address
        # and message to send - here it is sent as one string.
        server.sendmail(FROMADDR, to_addr, msg.as_string())
