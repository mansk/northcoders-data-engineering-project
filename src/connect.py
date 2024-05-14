import pg8000.native
import os
from dotenv import load_dotenv

load_dotenv(override=True)

def connect_db():
  return pg8000.native.Connection(
    user=os.getenv('PG_USER'),
    password=os.getenv('PG_PASSWORD'),
    database=os.getenv('PG_DATABASE'),
    host=os.getenv('PG_HOST'),
    port=os.getenv('PG_PORT')
  )


  