import pandas as pd
from src.connect import connect_db




def loading_to_sql(table_name, conn, df):
    
    #schema = get_database_credentials("data_warehouse_credentials")["schema"]

    try:
        df.to_sql(name=table_name, con=conn, if_exists='append')
    
    except Exception as e:
        raise e