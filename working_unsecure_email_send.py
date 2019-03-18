import smtplib
import os
import socket

def send_email(host, port, username, password, subject, body, mail_to, mail_from = None, reply_to = None):
    if mail_from is None: mail_from = username
    if reply_to is None: reply_to = mail_to

    message = """From: %s\nTo: %s\nReply-To: %s\nSubject: %s\n\n%s""" % (mail_from, mail_to, reply_to, subject, body)
    print (message)
    try:
        print("connecting to server")
        server = smtplib.SMTP(host, port)
        print("connecting to ehlo1")
        server.ehlo()
        print("connecting to starttls")
        server.starttls()
        print("logging in")
        server.login(username, password)
        print("sending")
        server.sendmail(mail_from, mail_to, message)
        
        server.close()
        return True
    except Exception as ex:
        print (ex)
        return False

def lambda_handler(event, context):

    # initialize variables
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #host_ip = socket.gethostbyname('smtp.gmail.com')
    username = os.environ['USERNAME']
    password = os.environ['PASSWORD']
    host = os.environ['SMTPHOST']
    port = os.environ['SMTPPORT']
    mail_from = os.environ.get('MAIL_FROM')
    mail_to = event['email'] # separate multiple recipient by comma. eg: "abc@gmail.com, xyz@gmail.com"
    origin = os.environ.get('ORIGIN')
    #origin_req = event['headers'].get('Host')

    #reply_to = event['queryStringParameters'].get('reply')
    subject = 'Here are your free Aurora Cards!'
    body = """Greetings,

Thank you for your interest in using our augmented reality cards. You will find a printout for three cards attached to this email. Simply print out the cards and use the app to play AR games right from your phone. 

We will let you know when more cards become available. 

Enjoy!
Aurora Team
    """

    # vaildate cors access
    cors = ''
    if not origin:
        cors = '*'
    elif origin_req in [o.strip() for o in origin.split(',')]:
        cors = origin_req

    # send mail
    success = False
    if cors:
        success = send_email(host, port, username, password, subject, body, mail_to, mail_from)

    # prepare response
    response = {
        "isBase64Encoded": False,
        "headers": { "Access-Control-Allow-Origin": cors }
    }
    if success:
        response["statusCode"] = 200
        response["body"] = '{"status":true}'
    elif not cors:
        response["statusCode"] = 403
        response["body"] = '{"status":false}'
    else:
        response["statusCode"] = 400
        response["body"] = '{"status":false}'
    return response
    