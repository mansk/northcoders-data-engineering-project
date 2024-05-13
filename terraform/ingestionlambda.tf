resource "aws_lambda_function" "ingestion_lambda" {
    function_name = "${var.team_prefix}ingestion-lambda"
    role = aws_iam_role.ingestion_lambda_role.arn
    handler = n/a
    runtime = n/a
}


