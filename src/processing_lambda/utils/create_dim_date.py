import pandas as pd
from pandas import DatetimeIndex
from datetime import datetime

def create_dim_date(dates):
    """Adds specified columns from dataframe and returns dataframe.

    This function is used to add dates to the date dimension table using timestamp and return the dataframe.

    This function intentionally mutates the input dataframe as we do not wish to replicate the data in memory and we will not need the old dataframe again.

    Args:
        date: A date based on facts table series.

    Returns:
        dataframe: A pandas dataframe.

    Raises:
        TypeError if arguments do not conform to expected types.
    """

    if not isinstance(dates, list):
        raise TypeError("Input needs to be a list of strings!")
    


    date_in_datatime_object = [datetime.fromisoformat(date) for date in dates]


    dim_date = pd.DataFrame({
        'date_id' : dates,
        'year': [date.year for date in date_in_datatime_object],
        'month' : [date.month for date in date_in_datatime_object],
        'day' : [date.day for date in date_in_datatime_object],
        'day_of_week' : [date.weekday() for date in date_in_datatime_object],
        'day_name' : [date.strftime('%A') for date in date_in_datatime_object],
        'month_name' : [date.strftime('%B') for date in date_in_datatime_object],
        'quarter' : [(date.month - 1) // 3 + 1 for date in date_in_datatime_object]
    })


    return dim_date