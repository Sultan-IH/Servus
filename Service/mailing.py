import smtplib
import os
from Service.Collection import Error

USERNAME = os.getenv("EMAIL_USERNAME")
PASSWORD = os.getenv("EMAIL_PASSWORD")
FROMADDR = "reports@servus.io"

if USERNAME is None or PASSWORD is None:
    print("INVALID USER NAME AND PASSWORD FOR EMAIL")


def send_email(to_addr: str, subject: str, error: Error):
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        try:
            server.ehlo()

            server.starttls()
            server.login(USERNAME, PASSWORD)
        except:
            return print("mailing module, something went wrong")

        msg = "\r\n".join([
            "From: " + FROMADDR,
            "To: " + to_addr,
            "Subject: " + subject,
            "",
            str(error)
        ])
        print(msg)
        server.sendmail(FROMADDR, to_addr, msg)
