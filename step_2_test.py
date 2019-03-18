import smtplib, ssl
import os

smtp_server = "smtp.gmail.com"
sender_email = "auroracardemailtest@gmail.com"
receiver_email = "jamitefridj@gmail.com"
message = """\
    Subject: Hi Test


    This is my first test."""

port = 587  #Required for starttls
password = "actest123"

# Create a secure SSL context
context = ssl.create_default_context()

try:
    server = smtplib.SMTP(smtp_server, port)
    server.ehlo()
    server.starttls(context=context) #Secure the connection
    server.ehlo()
    server.login(sender_email,password)
    server.sendmail(sender_email, receiver_email, message)
    
except Exception as e:
    print(e)