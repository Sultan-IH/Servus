import smtplib
import os
from Service.Collection import Error

USERNAME = 'ksula0155@gmail.com'  # os.getenv("EMAIL_USERNAME")
PASSWORD = 'Gmail123Darkside'  # os.getenv("EMAIL_PASSWORD")
FROMADDR = "reports@servus.io"

if USERNAME is None or PASSWORD is None:
    print("INVALID USER NAME AND PASSWORD FOR EMAIL")

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()

    server.starttls()
    server.login(USERNAME, PASSWORD)
except:
    print("mailing module, something went wrong")


def send_email(to_addr: str, subject: str, error: Error):
    msg = "\r\n".join([
        "From: " + FROMADDR,
        "To: " + to_addr,
        "Subject: " + subject,
        "",
        str(error)
    ])
    print(msg)
    server.sendmail(FROMADDR, to_addr, msg)
