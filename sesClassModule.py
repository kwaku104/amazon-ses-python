import smtplib  
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from getpass import getpass

class Email:
    def __init__(self, SENDER, SENDERNAME, RECIPIENT, USERNAME_SMTP, PASSWORD_SMTP, aws_region, SUBJECT, BODY_TEXT, BODY_HTML):
        self.SENDER = SENDER
        self.SENDERNAME = SENDERNAME
        self.RECIPIENT = RECIPIENT
        self.USERNAME_SMTP = USERNAME_SMTP
        self.PASSWORD_SMTP = PASSWORD_SMTP
        self.aws_region = aws_region
        self.SUBJECT = SUBJECT
        self.BODY_TEXT = BODY_TEXT
        self.BODY_HTML = BODY_HTML

    def sendEmail(self):
        HOST = "email-smtp."+ self.aws_region +".amazonaws.com"
        PORT = 587
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = self.SUBJECT
        msg['From'] = email.utils.formataddr((self.SENDERNAME, self.SENDER))
        msg['To'] = self.RECIPIENT

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(self.BODY_TEXT, 'plain')
        part2 = MIMEText(self.BODY_HTML, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)

        # Try to send the message.
        try:  
            server = smtplib.SMTP(HOST, PORT)
            server.ehlo()
            server.starttls()
            #stmplib docs recommend calling ehlo() before & after starttls()
            server.ehlo()
            server.login(self.USERNAME_SMTP, self.PASSWORD_SMTP)
            server.sendmail(self.SENDER, self.RECIPIENT, msg.as_string())
            server.close()
        # Display an error message if something goes wrong.
        except Exception as e:
            print ("Error: ", e)
        else:
            print ("Email sent!")
