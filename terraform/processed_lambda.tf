resource "aws_lambda_function" "processed_lambda" {
  function_name    = "${var.team_prefix}processed-lambda"
  filename         = n/a
  source_code_hash = n/a
  role             = aws_iam_role.processed_lambda_role.arn
  handler          = n/a
  layers           = n/a 
  runtime          = "python3.11"
  timeout          = 60
}


