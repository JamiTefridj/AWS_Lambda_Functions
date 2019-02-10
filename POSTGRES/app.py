import sys
import logging
import psycopg2
#rds settings
rds_host  = "myauroradbinstancev2.crmqojacvx6b.us-east-2.rds.amazonaws.com"
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = psycopg2.connect(rds_host, user=name, password=password, database=db_name, connect_timeout=5)
except:
    logger.error("ERROR: Unexpected error: Could not connect to POSTGRES instance.")
    sys.exit()

logger.info("SUCCESS: Connection to RDS POSTGRES instance succeeded")
def handler(event, context):
    """
    This function fetches content from POSTGRES RDS instance
    """

    item_count = 0

    with conn.cursor() as cur:
        # cur.execute("create table Employee3 ( EmpID  int NOT NULL, Name varchar(255) NOT NULL, PRIMARY KEY (EmpID))")  
        # cur.execute('insert into Employee3 (EmpID, Name) values(1, "Joe")')
        # cur.execute('insert into Employee3 (EmpID, Name) values(2, "Bob")')
        # cur.execute('insert into Employee3 (EmpID, Name) values(3, "Mary")')
        #conn.commit()
        cur.execute("select * from bhubs")
        for row in cur:
            item_count += 1
            logger.info(row)
            #print(row)
    conn.commit()

    return "Added %d items from RDS POSTGRES table" %(item_count)