import boto3
from botocore.exceptions import ClientError
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage

msg = MIMEMultipart()

SENDER = "aurorarealitysystems@gmail.com"

AWS_REGION = "us-east-1"

# The subject line for the email.
SUBJECT = "Here are your free Aurora Cards!"

# The email body for recipients with non-HTML email clients.
BODY_TEXT = ("""Greetings,

Thank you for your interest in using our augmented reality cards. You will find a printout for three cards attached to this email. Simply print out the cards and use the app to play AR games right from your phone. 

We will let you know when more cards become available. 

Enjoy!
Aurora Team
    """)
            
# The HTML body of the email.
# BODY_HTML = """<html>
# <head></head>
# <body>
#   <h1>Amazon SES Test (SDK for Python)</h1>
#   <p>This email was sent with
#     <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
#     <a href='https://aws.amazon.com/sdk-for-python/'>
#       AWS SDK for Python (Boto)</a>.</p>
# </body>
# </html>
#             """            

# The character encoding for the email.
CHARSET = "UTF-8"

def lambda_handler(event, context):
    RECIPIENT = event['email']
    msg = MIMEMultipart()
    msg.attach(MIMEText(file("Aurora_Card_Printout.pdf".read()))
    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)

    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    # 'Html': {
                    #     'Charset': CHARSET,
                    #     'Data': BODY_HTML,
                    # },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
                'Data': msg.as_string()
            },
            Source=SENDER,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])