resource "aws_lambda_function" "loading_lambda" {
  function_name    = "${var.team_prefix}loading-lambda"
  filename         = data.archive_file.lambda_loading_source.output_path
  source_code_hash = data.archive_file.lambda_loading_source.output_base64sha256
  role             = aws_iam_role.loading_lambda_role.arn
  handler          = "lambda_handler.lambda_handler"
  layers           = [aws_lambda_layer_version.lambda_layer.arn,
                      aws_lambda_layer_version.pandas_lambda_layer.arn]
  runtime          = "python3.11"
  timeout          = 60
}

data "archive_file" "lambda_loading_source" {
  type        = "zip"
  output_path = "${path.module}/../zip/loading.zip"
  source_dir  = "${path.module}/../src/loading_lambda/"
}


# data "archive_file" "loading_lambda_layer_zip" {
#   type        = "zip"
#   output_path = "${path.module}/../zip/layer.zip"
#   source_dir  = "${path.module}/../src/packages/"
# }

# resource "aws_lambda_layer_version" "lambda_layer" {
#   filename            = "${path.module}/../zip/layer.zip"
#   layer_name          = "pg8000_layer"
#   source_code_hash    = data.archive_file.lambda_layer_zip.output_base64sha256
#   compatible_runtimes = ["python3.11"]
# }

