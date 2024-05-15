from pg8000.native import identifier
import datetime

def get_table(table_name, conn, last_timestamp=datetime.datetime.min):
    try:
        query = f"SELECT * FROM {identifier(table_name)} "
        query += ("WHERE last_updated > :last_timestamp "
                  "OR created_at > :last_timestamp")
        result = conn.run(query, last_timestamp=last_timestamp)
        output_list = [
            dict(zip([column["name"] for column in conn.columns], r)) for r in result
        ]
        return output_list

    except Exception as e:
        raise e
