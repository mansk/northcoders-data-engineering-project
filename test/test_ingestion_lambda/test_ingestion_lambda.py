import pytest
import datetime
from src.ingestion_lambda.lambda_handler import get_table
from decimal import Decimal
from types import NoneType


# Data insertion
def test_get_table_returns_correct_types_for_currency_table():
    results = get_table("currency")
    for result in results:
        assert isinstance(result["currency_id"], int)
        assert isinstance(result["currency_code"], str)
        assert isinstance(result["created_at"], datetime.datetime)
        assert isinstance(result["last_updated"], datetime.datetime)


def test_get_table_returns_correct_types_for_counterparty_table():
    results = get_table("counterparty")
    for result in results:
        assert isinstance(result["counterparty_id"], int)
        assert isinstance(result["counterparty_legal_name"], str)
        assert isinstance(result["legal_address_id"], int)
        assert isinstance(result["commercial_contact"], (str, NoneType))
        assert isinstance(result["delivery_contact"], (str, NoneType))
        assert isinstance(result["created_at"], datetime.datetime)
        assert isinstance(result["last_updated"], datetime.datetime)


def test_get_table_returns_correct_types_for_department_table():
    results = get_table("department")
    for result in results:
        assert isinstance(result["department_id"], int)
        assert isinstance(result["department_name"], str)
        assert isinstance(result["location"], (str, NoneType))
        assert isinstance(result["manager"], (str, NoneType))
        assert isinstance(result["created_at"], datetime.datetime)
        assert isinstance(result["last_updated"], datetime.datetime)


def test_get_table_returns_correct_types_for_design_table():
    results = get_table("design")
    for result in results:
        design_id, created_at, last_updated, design_name, file_location, file_name = (
            result
        )
        assert isinstance(result["design_id"], int)
        assert isinstance(result["design_name"], str)
        assert isinstance(result["file_location"], str)
        assert isinstance(result["created_at"], datetime.datetime)
        assert isinstance(result["last_updated"], datetime.datetime)


def test_get_table_returns_correct_types_for_staff_table():
    results = get_table("staff")
    for result in results:
        assert isinstance(result["staff_id"], int)
        assert isinstance(result["first_name"], str)
        assert isinstance(result["last_name"], str)
        assert isinstance(result["department_id"], int)
        assert isinstance(result["email_address"], str)
        assert isinstance(result["created_at"], datetime.datetime)
        assert isinstance(result["last_updated"], datetime.datetime)


def test_get_table_returns_correct_types_for_salesOrder_table():
    results = get_table("sales_order")
    for result in results:
        assert isinstance(result["sales_order_id"], int)
        assert isinstance(result["design_id"], int)
        assert isinstance(result["staff_id"], int)
        assert isinstance(result["counterparty_id"], int)
        assert isinstance(result["units_sold"], int)
        assert isinstance(result["unit_price"], Decimal)
        assert isinstance(result["currency_id"], int)
        assert isinstance(result["agreed_delivery_date"], str)
        assert isinstance(result["agreed_payment_date"], str)
        assert isinstance(result["agreed_delivery_location_id"], int)
        assert isinstance(result["created_at"], datetime.datetime)
        assert isinstance(result["last_updated"], datetime.datetime)


def test_get_table_returns_correct_types_for_address_table():
    results = get_table("address")
    for result in results:
        assert isinstance(result["address_id"], int)
        assert isinstance(result["district"], (str, NoneType))
        assert isinstance(result["city"], str)
        assert isinstance(result["postal_code"], str)
        assert isinstance(result["country"], str)
        assert isinstance(result["phone"], str)
        assert isinstance(result["address_line_1"], str)
        assert isinstance(result["address_line_2"], (str, NoneType))
        assert isinstance(result["created_at"], datetime.datetime)
        assert isinstance(result["last_updated"], datetime.datetime)


def test_get_table_returns_correct_types_for_purchase_order_table():
    results = get_table("purchase_order")
    for result in results:
        assert isinstance(result["purchase_order_id"], int)
        assert isinstance(result["staff_id"], int)
        assert isinstance(result["counterparty_id"], int)
        assert isinstance(result["item_code"], str)
        assert isinstance(result["item_quantity"], int)
        assert isinstance(result["item_unit_price"], Decimal)
        assert isinstance(result["currency_id"], int)
        assert isinstance(result["agreed_delivery_date"], str)
        assert isinstance(result["agreed_payment_date"], str)
        assert isinstance(result["agreed_delivery_location_id"], int)
        assert isinstance(result["created_at"], datetime.datetime)
        assert isinstance(result["last_updated"], datetime.datetime)


def test_get_table_returns_correct_types_for_payment_type_table():
    results = get_table("payment_type")
    for result in results:
        assert isinstance(result["payment_type_id"], int)
        assert isinstance(result["payment_type_name"], str)
        assert isinstance(result["created_at"], datetime.datetime)
        assert isinstance(result["last_updated"], datetime.datetime)


def test_get_table_returns_correct_types_for_payment_table():
    results = get_table("payment")
    for result in results:
        assert isinstance(result["payment_id"], int)
        assert isinstance(result["transaction_id"], int)
        assert isinstance(result["counterparty_id"], int)
        assert isinstance(result["payment_amount"], Decimal)
        assert isinstance(result["payment_type_id"], int)
        assert isinstance(result["currency_id"], int)
        assert isinstance(result["paid"], bool)
        assert isinstance(result["payment_date"], str)
        assert isinstance(result["company_ac_number"], int)
        assert isinstance(result["counterparty_ac_number"], int)
        assert isinstance(result["created_at"], datetime.datetime)
        assert isinstance(result["last_updated"], datetime.datetime)
