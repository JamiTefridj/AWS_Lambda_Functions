import sys
import logging
import rds_config
import pymysql
import boto3
from botocore.exceptions import ClientError

#rds settings
rds_host  = "auroradbmysql.crmqojacvx6b.us-east-2.rds.amazonaws.com"
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")

#boto settings
SENDER = "aurorarealitysystems@gmail.com"
AWS_REGION = "us-east-1"
SUBJECT = "Amazon SES Test (SDK for Python)"
BODY_TEXT = ("Amazon SES Test (Python)\r\n"
             "This email was sent with Amazon SES using the "
             "AWS SDK for Python (Boto)."
            )
BODY_HTML = """<html>
<head></head>
<body>
  <h1>Amazon SES Test (SDK for Python)</h1>
  <p>This email was sent with
    <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
    <a href='https://aws.amazon.com/sdk-for-python/'>
      AWS SDK for Python (Boto)</a>.</p>
</body>
</html>
            """          
CHARSET = "UTF-8"


def handler(event, context):
    email = event['email']
    source = event['source']
    email_source_dict = {"email": email, "source": source}
    
    
    #This function fetches content from MySQL RDS instance
    cursor = conn.cursor()

    sql_insert_location = """insert into cardEmail set email=%(email)s, email_source=%(source)s"""
    logger.info("Starting: Insert Query")
    cursor.execute(sql_insert_location, email_source_dict)
    logger.info("SUCCESS: Insert QUERY succeeded")

    RECIPIENT = event['email'] # Add ['queryStringParameters'] later for API debuggin
     # Create a new SES resource and specify a region.
     
    logger.info("Starting: Connection to SES instance")
    client = boto3.client('ses',region_name=AWS_REGION)
    logger.info("SUCCESS: Connection to SES instance succeeded")
    
    # Try to send the email.
    # try:
    #Provide the contents of the email.
    
    logger.info("Starting: sending email")
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
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])



    # response = client.send_email(
    #     Destination={
    #         'ToAddresses': [
    #             RECIPIENT,
    #         ],
    #     },
    #     Message={
    #         'Body': {
    #             'Html': {
    #                 'Charset': CHARSET,
    #                 'Data': BODY_HTML,
    #             },
    #             'Text': {
    #                 'Charset': CHARSET,
    #                 'Data': BODY_TEXT,
    #             },
    #         },
    #         'Subject': {
    #             'Charset': CHARSET,
    #             'Data': SUBJECT,
    #         },
    #     },
    #     Source=SENDER,
    # )
    # logger.info("SUCCESS: EMAIL SENT")
    
    # Display an error if something goes wrong.	
    # except ClientError as e:
    #     print(e.response['Error']['Message'])
    # else:
    #     print("Email sent! Message ID:"),
    #     print(response['MessageId'])
    
    #insert email into db
    # email = event['email']
    # source = event['source']
    # email_source_dict = {"email": email, "source": source}
    
    
    # #This function fetches content from MySQL RDS instance
    # cursor = conn.cursor()

    # sql_insert_location = """insert into cardEmail set email=%(email)s, email_source=%(source)s"""
    # logger.info("Starting: Insert Query")
    # cursor.execute(sql_insert_location, email_source_dict)
    # logger.info("SUCCESS: Insert QUERY succeeded")

    # return cursor._last_executed