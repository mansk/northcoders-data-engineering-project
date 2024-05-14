import boto3 
import datetime
import json
import logging
from src.connect import connect_db
from pg8000.native import identifier


client= boto3.client('s3')
logger= logging.getLogger()
logger.setLevel(logging.INFO)

def get_table(table_name):
  conn = None
  try:
    conn = connect_db()
    query = f'SELECT * FROM {identifier(table_name)} LIMIT 10;'
    result=conn.run(query)
    output_list = [
        dict(zip([ column['name'] for column in conn.columns], r))
        for r in result
    ]
    print("result:", output_list )
    return output_list

  finally:
    if conn:
      conn.close()

