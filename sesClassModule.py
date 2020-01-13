import smtplib  
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from getpass import getpass
from os.path import basename
from email import encoders

class Email:
    def __init__(self, SENDER,USERNAME_SMTP, PASSWORD_SMTP, aws_region):
        self.SENDER = SENDER
        self.USERNAME_SMTP = USERNAME_SMTP
        self.PASSWORD_SMTP = PASSWORD_SMTP
        self.aws_region = aws_region

    def sendMail(self, SENDERNAME, RECIPIENT, SUBJECT, BODY_HTML, BODY_TEXT, filename=None):
        HOST = "email-smtp."+ self.aws_region +".amazonaws.com"
        PORT = 587
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = SUBJECT
        msg['From'] = email.utils.formataddr((SENDERNAME, self.SENDER))
        msg['To'] = RECIPIENT

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(BODY_TEXT, 'plain')
        part2 = MIMEText(BODY_HTML, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)
        
        # In same directory as script
        # Open file in binary mode
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part3 = MIMEBase("application", "octet-stream")
            part3.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part3)

        # Add header as key/value pair to attachment part
        part3.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        # Add attachment to message and convert message to string
        msg.attach(part3)

        # Try to send the message.
        try:  
            server = smtplib.SMTP(HOST, PORT)
            server.ehlo()
            server.starttls()
            #stmplib docs recommend calling ehlo() before & after starttls()
            server.ehlo()
            server.login(self.USERNAME_SMTP, self.PASSWORD_SMTP)
            server.sendmail(self.SENDER, RECIPIENT, msg.as_string())
            server.close()
        # Display an error message if something goes wrong.
        except Exception as e:
            print ("Error: ", e)
        else:
            print ("Email sent!")
