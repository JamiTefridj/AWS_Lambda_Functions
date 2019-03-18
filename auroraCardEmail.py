import smtplib, ssl

sender_email = "auroracardemailtest@gmail.com"
receiver_email = "spencermaxwell96@gmail.com" # will need to be parameter for incoming email
message = """\
    Subject: Hi Test


    This is my first test."""

port = 465  #Required for SSL
password = input("Type your password and press enter: ")

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)

import yagmail

#receiver = "spencermaxwell96@gmail.com"
body = """\
Greetings,

Thank you for your interest in using our augmented reality cards. You will find a printout for three cards attached to this email. Simply print out the cards and use the app to play AR games right from your phone. 

We will let you know when more cards become available. 

Enjoy!
Aurora Team"""
filename="Aurora_Card_Printout.pdf"

def handler(event, context):
    email = event['email']
    source = event['source']
    
    yagmail.register("auroracardemailtest@gmail.com", "actest123")
    
    yag = yagmail.SMTP("auroracardemailtest@gmail.com")
    yag.send(
        to=email,
        subject="Here are your free Aurora Cards!",
        contents=body,
        attachments=filename,
    )