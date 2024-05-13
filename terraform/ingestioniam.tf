resource "aws_iam_role" "ingestion_lambda_role" {
    name = "${var.team_prefix}ingestion-lambda-role"
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

resource "aws_iam_policy" "ingestion_lambda_s3_policy" {
    name = "${var.team_prefix}ingestion-lambda-s3-policy"
    description = "Policy for lambda to write to s3"
    policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:PutObject",
        ]
        Effect   = "Allow"
        Resource = "${aws_s3_bucket.ingestion_bucket.arn}/*"
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_s3_policy_attachment" {
    role = aws_iam_role.ingestion_lambda_role.arn
    policy_arn = aws_iam_policy.ingestion_lambda_s3_policy.arn
}

resource "aws_iam_policy" "ingestion_lambda_logs_policy" {
    name = "${var.team_prefix}ingestion-lambda-logs-policy"
    description = "Policy for logging"
    policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "logs:CreateLogGroup",
        ]
        Effect   = "Allow"
        Resource = "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:*"
      },
      {
        Action = [
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Effect   = "Allow"
        Resource = "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/${ingestion_lambda}:*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_logs_policy_attachment" {
    role = aws_iam_role.ingestion_lambda_role.arn
    policy_arn = aws_iam_policy.ingestion_lambda_logs_policy.arn
}