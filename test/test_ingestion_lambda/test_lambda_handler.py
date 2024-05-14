from src.ingestion_lambda.lambda_handler import lambda_handler
import logging
from unittest.mock import patch

def test_lambda_handler_logs_successful_table_reads(caplog):
    caplog.set_level(logging.INFO)
    with patch('src.ingestion_lambda.lambda_handler.get_table') as mock_get_table:
        mock_get_table.return_value = {}
        lambda_handler()

    for table in [
        "counterparty", "currency", "department", "design", "staff",
        "sales_order", "address", "payment", "purchase_order", "payment_type",
        "transaction"
    ]:
        assert f"get_table ran successfully on table '{table}'" in caplog.text


