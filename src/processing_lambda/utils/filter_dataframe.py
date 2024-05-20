import pandas as pd


def filter_and_convert_dataframe_to_parquet(
    dataframe: pd.DataFrame, columns: list[str]
):
    """Chooses specified columns from dataframe and returns parquet.

    This function is used to select a subset of columns from a dataframe
    and return the resulting data in parquet format.

    This function is intentionally impure as we do not wish to replicate
    the data in memory and we will not later require the columns we are
    dropping here.

    Args:
        dataframe: A pandas dataframe.
        columns: A list of strings of column names to be retained in the output dataframe.

    Returns:
        bytes of binary parquet format

    Raises:

    """
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("First argument must be a pandas DataFrame")

    if not isinstance(columns, list):
        raise TypeError("Second argument must be a list")

    for col in dataframe.columns:
        if col not in columns:
            dataframe.drop(col, axis="columns", inplace=True)

    if dataframe.empty:
        raise ValueError("No matching columns found in dataframe")

    parquet_data = dataframe.to_parquet()

    return parquet_data
