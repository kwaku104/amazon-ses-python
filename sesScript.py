import smtplib  
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from getpass import getpass

def sendEmail(SUBJECT, BODY_TEXT, BODY_HTML):
    # Accept "From" address from user.
    # This address must be verified.
    SENDER = input('Enter the "From" email address:\n')  
    SENDERNAME = input('Enter your name:\n')

    RECIPIENT  = input("Enter recipient email address:\n")
    
    # Accept Amazon SES SMTP user name from user.
    USERNAME_SMTP = input("Enter your Amazon SES SMTP user name:\n")

    # Accept Amazon SES SMTP password from user.
    PASSWORD_SMTP = getpass("Amazon SES SMTP password:\n")

    # Accept Amazon SES SMTP endpoint of the appropriate region from user.
    aws_region = input("Enter aws region ID:\n")
    HOST = "email-smtp." + aws_region + ".amazonaws.com"
    PORT = 587

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = SUBJECT
    msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
    msg['To'] = RECIPIENT

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(BODY_TEXT, 'plain')
    part2 = MIMEText(BODY_HTML, 'html')

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
        server.login(USERNAME_SMTP, PASSWORD_SMTP)
        server.sendmail(SENDER, RECIPIENT, msg.as_string())
        server.close()
    # Display an error message if something goes wrong.
    except Exception as e:
        print ("Error: ", e)
    else:
        print ("Email sent!")
