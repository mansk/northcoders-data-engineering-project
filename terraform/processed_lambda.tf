resource "aws_lambda_function" "processed_lambda" {
  function_name    = "${var.team_prefix}ingestion-lambda"
  filename         = n/a
  source_code_hash = n/a
  role             = n/a
  handler          = n/a
  layers           = n/a 
  runtime          = "python3.11"
  timeout          = 60
}