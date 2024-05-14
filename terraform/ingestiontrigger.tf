resource "aws_cloudwatch_event_rule" "ingestion_scheduler" {
 
    name = "ingestion-five-minute-scheduler"
    schedule_expression = "rate(5 minutes)"

}


resource "aws_cloudwatch_event_target" "invoke_ingestion_lambda" {
    rule = aws_cloudwatch_event_rule.ingestion_scheduler.name
    arn = aws_lambda_function.ingestion_lambda.arn

}

resource "aws_lambda_permission" "allow_eventbridge" {
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ingestion_lambda.arn
  principal = "events.amazonaws.com"
  source_arn = aws_cloudwatch_event_rule.ingestion_scheduler.arn
}



resource "aws_cloudwatch_log_metric_filter" "ingestion_metric_filter" {
  name           = "Error-filter"
  pattern        = "ERROR"
  log_group_name = "/aws/lambda/${aws_lambda_function.ingestion_lambda.function_name}"

  metric_transformation {
    name      = "EventCount"
    namespace = "Ingestion-errors"
    value     = "1"
  }
}


resource "aws_cloudwatch_metric_alarm" "ingestion_metric_" {
  alarm_name                = "ingestion-error-alarm"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = "1"


  metric_name               = "${aws_cloudwatch_log_metric_filter.ingestion_metric_filter.metric_transformation[0].name}"
  namespace                 = "${aws_cloudwatch_log_metric_filter.ingestion_metric_filter.metric_transformation[0].namespace}"
  period                    = 120
  statistic                 = "Sum"
  threshold                 = 1
  #alarm_description         = "This metric monitors ec2 cpu utilization"
  #insufficient_data_actions = []
}