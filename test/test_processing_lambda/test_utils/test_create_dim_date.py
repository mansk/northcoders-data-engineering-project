from unittest.mock import patch
from src.processing_lambda.utils.create_dim_date import create_dim_date
import pandas as pd
import pytest
from pandas import DatetimeIndex



@pytest.fixture
def dummy_dates():
    return [
            '2024-01-01',
            '2024-02-02',
            '2024-03-03',
            '2024-04-04',
            '2021-05-05',
            '2022-06-06',
            '2014-07-07',
            '2024-08-08',
            '2024-09-09',
            '2024-10-10',
            '2024-11-11',
            '2024-12-12'
        ]
    

def test_create_dim_date_returns_dataframe(dummy_dates):


    result = create_dim_date(dummy_dates)

    assert isinstance(result, pd.DataFrame)


def test_create_dim_date_returns_columns(dummy_dates):

    expected = [
        'date_id' ,
        'year' ,
        'month' ,
        'day' ,
        'day_of_week',
        'day_name' ,
        'month_name',
        'quarter' 
            
    ]

    result = create_dim_date(dummy_dates)

    assert all(col in result.columns for col in expected)



def test_create_dim_date_works_return_correct_amount(dummy_dates):


    result = create_dim_date(dummy_dates)

    assert len(result.year) == 12
    assert len(result.month) == 12
    assert len(result.day) == 12


def test_create_dim_date_works_returns_day_of_week():


    result = create_dim_date(['2024-05-22'])

    assert result.day_of_week[0] == 2



def test_create_dim_date_works_returns_name_of_day():


    result = create_dim_date(['2024-05-22'])

    assert result.day_name[0] == 'Wednesday'



def test_create_dim_date_works_returns_name_of_month():


    result = create_dim_date(['2024-05-22'])

    assert result.month_name[0] == 'May'



def test_create_dim_date_works_returns_correct_quarter(dummy_dates):


    result = create_dim_date(dummy_dates)

    print(result.quarter) 

    assert list(result.quarter) == [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]



def test_create_dim_date_raised_type_error(dummy_dates):

    greeting = 'hello'

    with pytest.raises(TypeError):
        create_dim_date(greeting)
