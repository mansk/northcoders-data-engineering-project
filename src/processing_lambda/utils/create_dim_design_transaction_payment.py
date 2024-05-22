import pandas as pd
from src.processing_lambda.utils.jsonl_to_df import get_df_from_s3_bucket


def drop_update_created_at_two_columns(df: pd.DataFrame):
    """

    This function drops "last_updated", "created_at" columns

    Args:
        dataframe: A pandas dataframe.

    Returns:
        dataframe: A pandas dataframe.

    Raises:
        TypeError if argument is not a pandas dataframe.
        ValueError if no corresponding department information is found for any
        of the department ids in the staff dataframe.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Argument must be a pandas dataframe")

    design_df = get_df_from_s3_bucket("design")

    design_df = design_df.drop(columns=["last_updated", "created_at"])

    return design_df
