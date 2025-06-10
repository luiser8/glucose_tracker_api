import os
import smtplib
from email.message import EmailMessage

class mailerSendSrv:
    def __init__(self):
        self.smtp_port = int(os.getenv("EMAIL_SMTP_PORT"))
        self.smtp_server = os.getenv("EMAIL_SMTP_HOST")
        self.username = os.getenv("EMAIL_SMTP_USER")
        self.password = os.getenv("EMAIL_SMTP_PASSWORD")
        self.server = EmailMessage()

    def sendSrv(self, payload):
        if payload["email_from"]:
            try:
                self.server.set_content(payload["message"])
                self.server['Subject'] = payload["subject"]
                self.server['From'] = self.username
                self.server['To'] = payload["email_from"]

                smtp_server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                smtp_server.starttls()
                smtp_server.login(self.username, self.password)
                smtp_server.send_message(self.server)
                smtp_server.quit()

            except smtplib.SMTPException as e:
                return {"status": 500, "message": f"SMTP error occurred: {str(e)}"}

        return payload["message"]
