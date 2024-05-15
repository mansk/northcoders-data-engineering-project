resource "aws_lambda_function" "ingestion_lambda" {
    function_name = "${var.team_prefix}ingestion-lambda"
    filename = data.archive_file.lambda_ingestion_source.output_path
    source_code_hash = data.archive_file.lambda_ingestion_source.output_base64sha256
    role = aws_iam_role.ingestion_lambda_role.arn
    handler = "dummyhandler.dummy_handler"
    runtime = "python3.11"
}



data "archive_file" "lambda_ingestion_source" {
    type = "zip"
    output_path = "${path.module}/../zip/ingestion.zip"
    source_dir = "${path.module}/../src/ingestion/"
}

resource "aws_lambda_permission" "allow_eventbridge" {
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ingestion_lambda.arn
  principal = "events.amazonaws.com"
  source_arn = aws_cloudwatch_event_rule.ingestion_scheduler.arn
}