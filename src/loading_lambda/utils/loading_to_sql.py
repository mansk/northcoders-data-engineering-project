import pandas as pd
from src.get_db_creds import get_database_credentials


def loading_to_sql(table_name, conn, df):

    schema = get_database_credentials("data_warehouse_credentials")["schema"]

    try:
        df.to_sql(
            name=table_name,
            con=conn,
            index=False,
            if_exists="append",
            schema=schema,
        )

    except Exception as e:
        raise e
