from src.loading_lambda.utils.loading_to_sql import loading_to_sql
import pytest
import pandas as pd
import os
import pg8000.native
from dotenv import load_dotenv
import sqlalchemy as sa
from sqlalchemy import create_engine



class Base(DeclarativeBase):
    pass

@pytest.fixture
def db_con():

    load_dotenv(override=True)
    db_string = sa.engine.url.URL.create(     
        drivername="postgresql+pg8000",
        username=os.environ["PGUSER"],
        password=os.environ["PGPASSWORD"],
        host=os.environ["PGHOST"],
        port=os.environ["PGPORT"],
        database=os.environ["PGDATABASE"],
        )
    db_engine = create_engine(db_string)

    return db_engine

    


def test_loading_to_sql_writes_to_database(db_con):
    
    df = pd.DataFrame({
        "col1" : ["Hello", "my", "friend"],
        "col2" : ["Goodbye", "my", "friend"]
    })

    sql = "SELECT * FROM test"

    loading_df = loading_to_sql("test", db_con, df)
    output = pd.read_sql(sql,con=db_con)
    print(output)

    assert 1 == 2