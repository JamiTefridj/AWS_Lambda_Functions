import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

msg = MIMEMultipart()
msg['Subject'] = 'Here are your free Aurora Cards!'
msg['From'] = "aurorarealitysystems@gmail.com"
#Body of the email
part = MIMEText("""Greetings,

Thank you for your interest in using our augmented reality cards. You will find a printout for three cards attached to this email. Simply print out the cards and use the app to play AR games right from your phone. 

We will let you know when more cards become available. 

Enjoy!
Aurora Team
    """)
msg.attach(part)

attachment = MIMEApplication(open('Aurora_Card_Printout.pdf','rb').read())
attachment.add_header('Content-Disposition', 'attachment', filename='Aurora_Card_Printout.pdf')
msg.attach(attachment)


AWS_REGION = "us-east-1"

CHARSET = "UTF-8"

def lambda_handler(event, context):
    #RECIPIENT = event['email']
    # Create a new SES resource and specify a region.
    msg['To'] = event['email']
    client = boto3.client('ses',region_name=AWS_REGION)
    result = client.send_raw_email(RawMessage= {'Data':msg.as_string()}, Source=msg['From'], Destinations=[msg['To']])
    print (result)
