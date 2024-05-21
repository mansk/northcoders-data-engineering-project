resource "aws_iam_role" "processed_lambda_role" {
  name = "${var.team_prefix}processed-lambda-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_policy" "processed_lambda_read_ingestion_s3_policy" {
  name        = "${var.team_prefix}processed-lambda-read-ingestion-s3-policy"
  description = "Policy for lambda to read from ingestion s3"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:GetObject",
        ]
        Effect   = "Allow"
        Resource = "${aws_s3_bucket.ingestion_bucket.arn}/*"
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "processed_lambda_read_ingestion_s3_policy_attachment" {
  role       = aws_iam_role.processed_lambda_role.name
  policy_arn = aws_iam_policy.processed_lambda_read_ingestion_s3_policy.arn
}


resource "aws_iam_policy" "processed_lambda_write_to_processed_s3_policy" {
  name        = "${var.team_prefix}processed_lambda_write_to_processed_s3_policy"
  description = "Policy for lambda to write to processed s3"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:PutObject",
        ]
        Effect   = "Allow"
        Resource = "${aws_s3_bucket.processed_bucket.arn}/*"
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "processed_lambda_read_ingestion_s3_policy_attachment" {
  role       = aws_iam_role.processed_lambda_role.name
  policy_arn = aws_iam_policy.processed_lambda_write_to_processed_s3_policy.arn
}



# Define IAM policy for processing lambda to write logs
resource "aws_iam_policy" "processed_lambda_logs_policy" {
  name        = "${var.team_prefix}processed-lambda-logs-policy"
  description = "Policy for logging from processing lambda"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = ["logs:CreateLogGroup"]
        Effect   = "Allow"
        Resource = "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:*"
      },
      {
        Action   = ["logs:CreateLogStream", "logs:PutLogEvents"]
        Effect   = "Allow"
        Resource = "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/${aws_lambda_function.processed_lambda.function_name}:*"
      }
    ]
  })
}

# Attach logs policy to processing lambda role
resource "aws_iam_role_policy_attachment" "processed_lambda_logs_attachment" {
  role       = aws_iam_role.processed_lambda_role.name
  policy_arn = aws_iam_policy.processed_lambda_logs_policy.arn
}



# Define Archive File for processing Lambda Function
# data "archive_file" "lambda_processed_source" {
#   type        = "zip"
#   output_path = "${path.module}/../zip/processing.zip"
#   source_dir  = "${path.module}/../src/processing_lambda/"