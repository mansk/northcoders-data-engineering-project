import json
import datetime
from decimal import Decimal


def convert_dict_to_json(d):
    for key in d:
        if isinstance(d[key], datetime.datetime):
            d[key] = d[key].isoformat()
        elif isinstance(d[key], Decimal):
            d[key] = float(d[key])

    return json.dumps(d)


def convert_results_to_json_lines(results):
    output = "\n".join([convert_dict_to_json(result) for result in results])
    output += "\n"

    return output
