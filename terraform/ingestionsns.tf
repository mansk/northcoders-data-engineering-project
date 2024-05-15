resource "aws_sns_topic" "sns_error" {
  name = "watershed-sns-notifier"
}

resource "aws_sns_topic_subscription" "sns_error_sub" {
  topic_arn = "${aws_sns_topic.sns_error.arn}"
  protocol  = "email"
  endpoint  = "padmapriya.mariappan@gmail.com"

}


# resource "aws_sns_topic_subscription" "sns_topic_subscription" {
#   for_each = toset(["emailid1@email.com","emailid2@email.com","emailid3@email.com"])
#   topic_arn = aws_sns_topic.sns_topic.arn
#   protocol  = "email"
#   endpoint = each.value
# }
