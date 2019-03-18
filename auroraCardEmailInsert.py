import sys
import logging
import rds_config
import pymysql
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

def handler(event, context):
    email = event['email']
    source = event['source']
    email_source_dict = {"email": email, "source": source}
    """
    This function fetches content from MySQL RDS instance
    """
    cursor = conn.cursor()

    sql_insert_location = """insert into cardEmail set email=%(email)s, email_source=%(source)s"""

    cursor.execute(sql_insert_location, email_source_dict)

    return cursor._last_executed