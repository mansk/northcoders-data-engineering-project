from src.processing_lambda.utils.filter_dataframe import (
    filter_and_convert_dataframe_to_parquet,
)
import io
import pandas as pd
import pytest


def test_filter_and_convert_dataframe_returns_parquet():
    df = pd.DataFrame(
        {
            "one": [-1, 0, 2.5],
            "two": ["foo", "bar", "baz"],
            "three": [True, False, True],
        },
        index=list("abc"),
    )

    result = filter_and_convert_dataframe_to_parquet(df, ["two", "three"])

    pq_file = io.BytesIO(result)
    assert isinstance(pd.read_parquet(pq_file), pd.DataFrame)


def test_filter_and_convert_dataframe_correctly_filters_columns():
    input_df = pd.DataFrame(
        {
            "one": [-1, 0, 2.5],
            "two": ["foo", "bar", "baz"],
            "three": [True, False, True],
        },
        index=list("abc"),
    )

    parquet = filter_and_convert_dataframe_to_parquet(input_df, ["two", "three"])

    pq_file = io.BytesIO(parquet)
    output_df = pd.read_parquet(pq_file)

    assert "one" not in output_df.columns
    assert "two" in output_df.columns
    assert "three" in output_df.columns


def test_filter_and_convert_dataframe_correctly_retains_correct_data_in_columns():
    input_df = pd.DataFrame(
        {
            "one": [-1, 0, 2.5],
            "two": ["foo", "bar", "baz"],
            "three": [True, False, True],
        },
        index=list("abc"),
    )

    parquet = filter_and_convert_dataframe_to_parquet(input_df, ["two", "three"])

    pq_file = io.BytesIO(parquet)
    output_df = pd.read_parquet(pq_file)

    assert output_df["two"].equals(input_df["two"])
    assert output_df["three"].equals(input_df["three"])


def test_filter_and_convert_dataframe_raises_TypeError_if_first_arg_not_dataframe():
    with pytest.raises(TypeError):
        filter_and_convert_dataframe_to_parquet(True, ["test"])


def test_filter_and_convert_dataframe_raises_TypeError_if_second_arg_not_list():
    with pytest.raises(TypeError):
        filter_and_convert_dataframe_to_parquet(pd.DataFrame({}), 123)


def test_filter_and_conver_dataframe_raises_ValueError_when_no_matching_columns_are_found_in_df():
    input_df = pd.DataFrame(
        {
            "one": [-1, 0, 2.5],
            "two": ["foo", "bar", "baz"],
            "three": [True, False, True],
        },
        index=list("abc"),
    )

    with pytest.raises(ValueError):
        filter_and_convert_dataframe_to_parquet(input_df, ["four"])
