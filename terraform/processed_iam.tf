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