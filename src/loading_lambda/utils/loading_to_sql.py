import pandas as pd
try:
    from utils.get_db_creds import get_database_credentials
except ModuleNotFoundError:
    from src.get_db_creds import get_database_credentials


def loading_to_sql(table_name, conn, df):
    """This function is used to load the data into the warehouse using the credentials stored in AWS secrets manager

    Args:
        table_name: the name of the table into which the data needs to be inserted.
        conn: the connection to the database
        df: the data that is to be inserted
    
    Returns:
        None

    """
    schema = get_database_credentials("data_warehouse_credentials")["schema"]

    try:
        df.to_sql(
            name=table_name,
            con=conn,
            index=False,
            if_exists="append",
            schema=schema,
            method=postgres_insert
        )

    except Exception as e:
        raise

def postgres_insert(table, conn, keys, data_iter):
    from sqlalchemy.dialects.postgresql import insert

    data = [dict(zip(keys, row)) for row in data_iter]

    insert_statement = insert(table.table).values(data)
    ignore_statement = insert_statement.on_conflict_do_nothing()
    conn.execute(ignore_statement)
