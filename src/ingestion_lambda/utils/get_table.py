from pg8000.native import identifier

def get_table(table_name, conn=None):
    try:
        query = f"SELECT * FROM {identifier(table_name)} LIMIT 10;"
        result = conn.run(query)
        output_list = [
            dict(zip([column["name"] for column in conn.columns], r)) for r in result
        ]
        return output_list

    except Exception as e:
        raise e
